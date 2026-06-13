"""AI合同审查系统 - 四层架构实现 + 批量处理 + 多领域推理 + 用户认证 + 安全合规 + 前置防护"""
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends, Header, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Tuple
import os
import io
import logging
import asyncio
from dotenv import load_dotenv
import json

logger = logging.getLogger(__name__)

from layers.input_layer import InputLayer
from layers.inference_layer import InferenceLayer
from layers.validation_layer import ValidationLayer
from layers.output_layer import OutputLayer
from tasks import Task, TaskStatus, create_task, get_task, update_task, get_all_tasks, run_with_concurrent_limit, delete_task as delete_task_func, concurrent_semaphore, init_task_storage, wait_for_task_update
from reasoning import load_reasoning_module, get_supported_domains
from reasoning.llm_client import CircuitBreakerOpenError, AllModelsFailedError, get_circuit_breaker_status
from auth.routes import get_current_user, router as auth_router
from storage.crud import (
    init_db, create_record, get_records_by_user, get_record, delete_record,
    add_to_blacklist, remove_from_blacklist, get_all_blacklist,
    get_user_bonus_credits, use_user_bonus_credit,
    complete_invite_reward
)
from routers import feedback, user, admin, records
from security.middleware import SecurityMiddleware, ENABLE_SENSITIVE_FILTER, ADMIN_TOKEN
from security import get_sensitive_filter, structured_logger
from security.rate_limiter import get_rate_limiter
from security.blacklist import blacklist_manager
from security.pre_validation import validate_file_basic, validate_content, validate_with_extractor
from security.malicious_behavior_detector import get_malicious_tracker, record_violation, is_auto_banned
from security.injection_detector import get_injection_detector
from security.output_guard import init_output_guard, get_output_guard, check_output_leak
from security.security_events import record_security_event
from utils.security import ban_user_for_injection

load_dotenv()

# 初始化数据库 + 从 DB 恢复未完成任务
init_db()
init_task_storage()


def filter_metadata_for_frontend(metadata: Optional[dict]) -> Optional[dict]:
    """过滤metadata，只保留前端需要的字段，剔除内部校验字段"""
    if not metadata:
        return None
    
    # 定义前端需要的字段白名单
    allowed_fields = {
        'file_hash',      # 用于MD5重复检测
        'timestamp',      # 审查时间
        'model_version',  # 模型版本
    }
    
    # 只保留白名单中的字段
    filtered = {key: value for key, value in metadata.items() if key in allowed_fields}
    return filtered if filtered else None

app = FastAPI(title="AI合同审查系统", version="5.0.0", description="基于四层架构的合同审查系统，支持批量处理、多领域推理、用户认证和安全合规")

@app.on_event("startup")
async def startup_event():
    """启动时清理过期日志、预初始化Redis、初始化安全模块"""
    from security.sensitive_filter import cleanup_old_logs
    deleted = cleanup_old_logs(days=90)
    logger.info(f"启动时清理了 {deleted} 条过期拦截日志")
    
    # 预初始化Redis客户端，避免首次请求时的连接延迟
    try:
        from utils.redis_client import redis_client
        redis_client.connect()
        if redis_client.get_client():
            logger.info("Redis连接成功，将使用Redis进行限流和缓存")
        else:
            logger.info("Redis连接失败，已切换到内存模式，后续请求无延迟")
    except Exception as e:
        logger.warning(f"Redis预初始化失败: {e}，将使用内存模式")
    
    # ========== 初始化输出安全守卫（SHA256滑动窗口检测） ==========
    try:
        from layers.inference_layer import InferenceLayer
        temp_layer = InferenceLayer()
        system_prompt = temp_layer.prompt_template
        guard = init_output_guard(system_prompt)
        logger.info(f"[STARTUP] 输出安全守卫初始化完成: 片段哈希数={len(guard._fragment_hashes)}")
    except Exception as e:
        logger.error(f"[STARTUP] 输出安全守卫初始化失败: {e}")
    
    # ========== 初始注入检测器 ==========
    try:
        get_injection_detector()
        logger.info("[STARTUP] 注入检测器初始化完成")
    except Exception as e:
        logger.error(f"[STARTUP] 注入检测器初始化失败: {e}")
    
    # ========== 运行安全增强迁移 ==========
    try:
        import importlib.util
        migration_path = os.path.join(os.path.dirname(__file__), "migrations", "006_add_security_enhancements.py")
        spec = importlib.util.spec_from_file_location("mig_006", migration_path)
        mig = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mig)
        mig.migrate()
        logger.info("[STARTUP] 安全增强迁移完成")
    except Exception as e:
        logger.error(f"[STARTUP] 安全增强迁移失败: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SecurityMiddleware)

# 注册认证路由
app.include_router(auth_router)
app.include_router(feedback.router, prefix="/api")
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(records.router)

# 初始化四层模块
input_layer = InputLayer()
inference_layer = InferenceLayer()
validation_layer = ValidationLayer()
output_layer = OutputLayer()

class TaskResponse(BaseModel):
    task_id: str
    filename: str
    file_size: int
    status: str
    progress: int
    result: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None
    validation: Optional[dict] = None
    summary: Optional[dict] = None
    remaining_bonus: Optional[int] = None

class ReviewResponse(BaseModel):
    success: bool
    message: str
    result: Optional[str] = None
    metadata: Optional[dict] = None
    validation: Optional[dict] = None
    summary: Optional[dict] = None
    record_id: Optional[int] = None

class BatchResponse(BaseModel):
    success: bool
    message: str
    task_ids: Optional[List[str]] = None
    rejected_files: Optional[List[dict]] = None

class ValidationErrorResponse(BaseModel):
    success: bool
    message: str
    error_code: str
    filename: Optional[str] = None

class BlacklistItemRequest(BaseModel):
    type: str  # "ip" or "user_id"
    value: str
    reason: str = ""

def check_sensitive_content(text: str, extra_requirements: str = "") -> Tuple[bool, str]:
    """检查敏感内容"""
    if not ENABLE_SENSITIVE_FILTER:
        return True, ""
    
    filter = get_sensitive_filter()
    texts_to_check = [text, extra_requirements]
    for t in texts_to_check:
        if t:
            ok, hits = filter.filter(t)
            if not ok:
                return False, f"内容包含敏感信息：{', '.join(hits[:5])}"
    return True, ""

async def run_inference_with_progress(task_id: str, inference_func, contract_text: str, additional_instructions: str):
    """带进度更新的LLM推理调用，定期发送心跳防止前端超时"""
    import threading
    
    stop_event = threading.Event()
    progress = 40
    
    def progress_updater():
        nonlocal progress
        while not stop_event.is_set():
            # 模拟进度逐步增加（从40%到60%）
            if progress < 60:
                progress += 5
                try:
                    update_task(task_id, progress=progress)
                except Exception:
                    pass
            # 每10秒更新一次
            stop_event.wait(10)
    
    # 启动进度更新线程
    updater_thread = threading.Thread(target=progress_updater, daemon=True)
    updater_thread.start()
    
    try:
        # 执行推理（阻塞调用，已移至线程池）
        result = await asyncio.to_thread(
            inference_func,
            contract_text,
            additional_instructions
        )
        return result
    finally:
        # 停止进度更新线程
        stop_event.set()
        updater_thread.join(timeout=1)


async def process_contract_task(task_id: str, file_content: bytes, filename: str, additional_instructions: str = "", file_hash: str = None):
    """异步处理单个合同审查任务"""
    logger.info(f"[PROCESS_TASK] task_id={task_id}, additional_instructions='{additional_instructions}'")

    async with concurrent_semaphore:
        task = get_task(task_id)
        if not task:
            return

        try:
            # 设置trace_id到上下文变量，确保异步任务中的日志有正确的trace_id
            from security.logging_utils import trace_id_context
            if task.trace_id:
                trace_id_context.set(task.trace_id)
            
            update_task(task_id, status=TaskStatus.UPLOADING, progress=10)

            # 创建一个类似UploadFile的文件对象供input_layer使用
            class FileContent:
                def __init__(self, content, name):
                    self.file = io.BytesIO(content)
                    self.filename = name

            file_obj = FileContent(file_content, filename)

            # ========== 输入层处理 ==========
            update_task(task_id, status=TaskStatus.PROCESSING, progress=20)
            input_result = input_layer.process(file_obj, additional_instructions)
            if input_result['status'] == 'error':
                update_task(task_id, status=TaskStatus.FAILED, error=f"输入处理失败: {input_result['message']}")
                return
            
            # ========== 推理层处理 ==========
            update_task(task_id, progress=40)
            try:
                # 使用带进度更新的LLM调用，定期发送心跳
                raw_report = await run_inference_with_progress(
                    task_id,
                    inference_layer.run_inference,
                    input_result.get('contract_text', ''),
                    additional_instructions
                )
                inference_result = {
                    "status": "success",
                    "raw_report": raw_report
                }
            except AllModelsFailedError as e:
                # 所有模型均失败，返回兜底消息并标记任务失败
                logger.warning(f"[Fallback] {task_id} 所有模型不可用，返回兜底消息")
                update_task(task_id, status=TaskStatus.FAILED, error=e.fallback_message)
                logger.error(f"[ALL_MODELS_FAILED] {task_id} 所有模型调用失败，任务标记为失败")
                return
            except CircuitBreakerOpenError as e:
                # 熔断器打开，返回503
                update_task(task_id, status=TaskStatus.FAILED, error=f"服务暂时不可用: {str(e)}")
                logger.error(f"[CircuitBreaker] {task_id} 任务因熔断被拒绝")
                return
            except Exception as e:
                update_task(task_id, status=TaskStatus.FAILED, error=f"推理失败: {str(e)}")
                return

            if inference_result['status'] == 'error':
                update_task(task_id, status=TaskStatus.FAILED, error=f"推理失败: {inference_result['message']}")
                return
            
            # ========== 校验层处理（在原始报告上执行）==========
            update_task(task_id, progress=60)
            validation_result = validation_layer.process(
                inference_result['raw_report'],
                input_result.get('contract_text')
            )
            
            if validation_result.get('status') == 'error':
                leak_msg = validation_result.get('warnings', ['校验失败'])
                update_task(task_id, status=TaskStatus.FAILED, error=f"校验未通过: {'; '.join(leak_msg)}")
                return

            # ========== 输出封装层处理（提取用户可见内容）==========
            update_task(task_id, progress=65)
            # 先过滤内部推理步骤，只保留对用户有用的内容
            filtered_report = output_layer._filter_internal_content(inference_result['raw_report'])
            
            # ========== SHA256滑动窗口输出泄露检测（在过滤后的内容上执行）==========
            update_task(task_id, progress=70)
            leak_passed, leak_detail = check_output_leak(filtered_report)
            if not leak_passed:
                logger.critical(f"[SECURITY] 输出泄露检测告警: task_id={task_id}, detail={leak_detail}")
                # 记录安全事件（输出泄露不封禁账号，仅记录事件）
                record_security_event(
                    event_type="output_leak",
                    severity="warning",
                    source="output_guard",
                    detail=f"task_id={task_id}, reason={leak_detail}, "
                           f"output_preview={filtered_report[:200]}",
                    user_id=task.user_id,
                    ip=None  # 异步任务中可能没有IP
                )
                update_task(task_id, status=TaskStatus.FAILED,
                           error="无法生成报告，请稍后重试")
                return
            
            # ========== 生成最终输出（使用过滤后的报告）==========
            update_task(task_id, progress=80)
            output_result = output_layer.package_output(
                filtered_report,  # 使用过滤后的报告
                validation_result,
                input_result
            )
            frontend_output = output_layer.format_for_frontend(output_result)
            
            # ========== 仅成功后才扣费（批量审查时）==========
            remaining_bonus = None
            if task.user_id:
                try:
                    success = use_user_bonus_credit(task.user_id)
                    remaining_bonus = get_user_bonus_credits(task.user_id)
                    if success:
                        logger.info(f"[QUOTA] 用户 {task.user_id} 审查完成，已扣减额度，剩余额度: {remaining_bonus}")
                    else:
                        logger.info(f"[QUOTA] 用户 {task.user_id} 审查完成，免费额度已用完，剩余额度: {remaining_bonus}")
                except Exception as e:
                    logger.error(f"[QUOTA] 用户 {task.user_id} 额度扣减失败: {e}")
            
            # ========== 保存报告记录（不保存原始合同文本）==========
            record_id = None
            if task.user_id:
                try:
                    # 将file_hash添加到metadata中
                    metadata = frontend_output.get('metadata') or {}
                    if file_hash:
                        metadata['file_hash'] = file_hash
                    
                    report_md = frontend_output.get('result', '')
                    # 安全兜底：如果报告内容过短（只有模板框架），记录警告
                    if not report_md or len(report_md.strip()) < 100:
                        logger.warning(f"[RECORD] 报告内容异常过短(len={len(report_md) if report_md else 0})，"
                                      f"raw_result_preview={str(frontend_output.get('result',''))[:200]}")
                    
                    record_id = create_record(
                        user_id=task.user_id,
                        filename=task.filename,
                        report_md=report_md,
                        metadata=metadata,
                        raw_output=inference_result.get('raw_report')
                    )
                    logger.info(f"[RECORD] 用户 {task.user_id} 报告已保存，记录ID: {record_id}, 报告长度: {len(report_md) if report_md else 0}")
                except Exception as e:
                    logger.error(f"[RECORD] 用户 {task.user_id} 报告保存失败: {e}")
            
            # ========== 触发邀请奖励（首次有效审查后）==========
            if task.user_id:
                try:
                    invite_result = complete_invite_reward(task.user_id)
                    if invite_result["success"]:
                        logger.info(f"[INVITE] 用户 {task.user_id} 完成首次审查，邀请奖励已发放")
                except Exception as e:
                    logger.error(f"[INVITE] 邀请奖励发放失败: {e}")
            
            # 更新任务完成
            update_task(task_id, 
                        status=TaskStatus.COMPLETED, 
                        progress=100,
                        result=frontend_output.get('result'),
                        metadata=frontend_output.get('metadata'),
                        validation=frontend_output.get('validation'),
                        summary=frontend_output.get('summary'),
                        remaining_bonus=remaining_bonus,
                        record_id=record_id)
            
        except Exception as e:
            update_task(task_id, status=TaskStatus.FAILED, error=f"处理失败: {str(e)}")

@app.post("/api/review", response_model=ReviewResponse)
async def review_contract(
    request: Request,
    file: UploadFile = File(...),
    additional_instructions: Optional[str] = Form(""),
    user_id: int = Depends(get_current_user)
):
    """单文件合同审查API（需认证）- 完整前置防护"""
    client_ip = request.client.host if request.client else "unknown"
    
    # ========== 前置防护0：额度检查 ==========
    remaining_bonus = get_user_bonus_credits(user_id)
    if remaining_bonus <= 0:
        raise HTTPException(status_code=403, detail={
            "error_code": "NO_CREDITS",
            "message": "您的免费额度已用完，请获取更多额度后再试"
        })
    
    # ========== 前置防护1：黑名单检查 ==========
    # 检查手动黑名单
    blacklisted = blacklist_manager.check(ip=client_ip, user_id=str(user_id))
    if blacklisted:
        raise HTTPException(status_code=403, detail={
            "error_code": "BLACKLISTED",
            "message": "账号因异常操作被临时限制，请联系客服处理"
        })
    # 检查自动封禁
    auto_banned, ban_reason = is_auto_banned(ip=client_ip, user_id=user_id)
    if auto_banned:
        raise HTTPException(status_code=403, detail={
            "error_code": "AUTO_BANNED",
            "message": ban_reason
        })
    
    # ========== 前置防护2：限流检查 ==========
    rate_limiter = get_rate_limiter()
    allowed, rate_msg = rate_limiter.is_allowed(str(user_id), client_ip, limit_type="review")
    if not allowed:
        record_violation(ip=client_ip, user_id=user_id, violation_type="rate_limit", reason=rate_msg)
        raise HTTPException(status_code=429, detail={
            "error_code": "RATE_LIMIT_EXCEEDED",
            "message": rate_msg
        })
    
    # ========== 前置防护3：基础文件校验 ==========
    valid, validation_error = validate_file_basic(file)
    if not valid:
        # 记录违规行为
        err_code = validation_error.get("error_code")
        if err_code == "INVALID_FORMAT":
            record_violation(ip=client_ip, user_id=user_id, violation_type="format_error", reason=validation_error.get("message"))
        elif err_code == "FILE_TOO_LARGE":
            record_violation(ip=client_ip, user_id=user_id, violation_type="size_exceeded", reason=validation_error.get("message"))
        raise HTTPException(status_code=400, detail=validation_error)

    # ========== 前置防护3.5：额外审查要求安全校验（增强版 - 含自动封禁） ==========
    from utils.security import validate_extra_requirements
    from security.injection_detector import check_input_injection as enhanced_injection_check

    # 先进行增强注入检测
    inj_passed, inj_error, inj_rules = enhanced_injection_check(
        additional_instructions or "", user_id=user_id, ip=client_ip
    )
    if not inj_passed:
        # 自动封禁
        ban_user_for_injection(
            user_id=user_id,
            ip=client_ip,
            input_text=additional_instructions or "",
            trigger_rule=", ".join(inj_rules) if inj_rules else "injection_pattern_matched"
        )
        raise HTTPException(status_code=403, detail={
            "error_code": "INJECTION_DETECTED",
            "message": "账号已被封禁，请联系管理员"
        })

    req_valid, req_error = validate_extra_requirements(additional_instructions, user_id=user_id, ip=client_ip)
    if not req_valid:
        raise HTTPException(status_code=400, detail={
            "error_code": "INVALID_EXTRA_REQUIREMENTS",
            "message": req_error
        })

    try:
        file_content = file.file.read()
        
        # ========== 前置防护4：文本内容预校验 ==========
        # 使用输入层提取文本
        class TempFileObj:
            def __init__(self, content, name):
                self.file = io.BytesIO(content)
                self.filename = name
        
        valid, content_error, contract_text = validate_with_extractor(
            file_content,
            file.filename,
            lambda f, a: input_layer.process(f, a)
        )
        
        if not valid:
            # 记录违规行为
            err_code = content_error.get("error_code")
            if err_code == "CONTENT_TOO_SHORT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="content_too_short", reason=content_error.get("message"))
            elif err_code == "NOT_CONTRACT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="not_contract", reason=content_error.get("message"))
            raise HTTPException(status_code=422, detail=content_error)
        
        # ========== 前置防护4.5：重复上传检测 ==========
        from storage.crud import calculate_file_hash, get_file_hash_cache
        
        enable_duplicate_check = os.getenv("ENABLE_DUPLICATE_CHECK", "true").lower() == "true"
        if enable_duplicate_check:
            file_hash = calculate_file_hash(file_content)
            existing_cache = get_file_hash_cache(user_id, file_hash)
            
            if existing_cache:
                raise HTTPException(status_code=409, detail={
                    "error_code": "DUPLICATE_UPLOAD",
                    "message": "您已上传过相同合同，是否仍要继续审查？本次将消耗免费额度/费用。",
                    "file_hash": file_hash,
                    "first_upload_time": existing_cache.first_upload_time.isoformat() if existing_cache.first_upload_time else None,
                    "upload_count": existing_cache.upload_count
                })
        
        # ========== 前置防护5：敏感词检查 ==========
        ok, msg = check_sensitive_content(contract_text, additional_instructions)
        if not ok:
            record_violation(ip=client_ip, user_id=user_id, violation_type="sensitive_content", reason=msg)
            structured_logger.log_security(
                "SENSITIVE_CONTENT_BLOCK",
                client_ip,
                str(user_id),
                msg
            )
            raise HTTPException(status_code=400, detail={
                "error_code": "SENSITIVE_CONTENT",
                "message": msg
            })
        
        # ========== 正常审查流程 ==========
        task = create_task(file.filename, len(file_content))
        await process_contract_task(task.task_id, file_content, file.filename, additional_instructions, file_hash if enable_duplicate_check else None)
        task_result = get_task(task.task_id)
        
        if task_result.status == TaskStatus.COMPLETED:
            # ========== 仅成功后才扣费 ==========
            used_bonus = use_user_bonus_credit(user_id)
            remaining_bonus = get_user_bonus_credits(user_id)

            # ========== 更新文件哈希缓存 ==========
            enable_duplicate_check = os.getenv("ENABLE_DUPLICATE_CHECK", "true").lower() == "true"
            if enable_duplicate_check:
                from storage.crud import calculate_file_hash, create_or_update_file_hash_cache
                file_hash = calculate_file_hash(file_content)
                create_or_update_file_hash_cache(user_id, file_hash, file.filename)

            return {
                "success": True,
                "message": "审查完成",
                "result": task_result.result,
                "metadata": filter_metadata_for_frontend(task_result.metadata),
                "validation": task_result.validation,
                "summary": task_result.summary,
                "record_id": task_result.record_id,
                "used_bonus": used_bonus,
                "remaining_bonus": remaining_bonus
            }
        else:
            error_msg = task_result.error or "处理失败"
            raise HTTPException(status_code=500, detail={
                "error_code": "PROCESSING_ERROR",
                "message": error_msg
            })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理异常: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail={
            "error_code": "INTERNAL_ERROR",
            "message": f"处理失败: {str(e)}"
        })

@app.post("/api/contract/review/confirm-duplicate", response_model=ReviewResponse)
async def review_contract_confirm_duplicate(
    request: Request,
    file: UploadFile = File(...),
    additional_instructions: Optional[str] = Form(""),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user_id: int = Depends(get_current_user)
):
    """确认重复文件审查API（需认证）- 用户确认后继续处理重复上传的合同"""
    client_ip = request.client.host if request.client else "unknown"
    
    # ========== 前置防护0：额度检查 ==========
    remaining_bonus = get_user_bonus_credits(user_id)
    if remaining_bonus <= 0:
        raise HTTPException(status_code=403, detail={
            "error_code": "NO_BONUS",
            "message": "免费额度已用完，请稍后再试"
        })
    
    try:
        file_content = file.file.read()
        
        # ========== 前置防护4：文本内容预校验 ==========
        class TempFileObj:
            def __init__(self, content, name):
                self.file = io.BytesIO(content)
                self.filename = name
        
        valid, content_error, contract_text = validate_with_extractor(
            file_content,
            file.filename,
            lambda f, a: input_layer.process(f, a)
        )
        
        if not valid:
            err_code = content_error.get("error_code")
            if err_code == "CONTENT_TOO_SHORT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="content_too_short", reason=content_error.get("message"))
            elif err_code == "NOT_CONTRACT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="not_contract", reason=content_error.get("message"))
            raise HTTPException(status_code=422, detail=content_error)
        
        # ========== 前置防护5：敏感词检查 ==========
        ok, msg = check_sensitive_content(contract_text, additional_instructions)
        if not ok:
            record_violation(ip=client_ip, user_id=user_id, violation_type="sensitive_content", reason=msg)
            structured_logger.log_security(
                "SENSITIVE_CONTENT_BLOCK",
                client_ip,
                str(user_id),
                msg
            )
            raise HTTPException(status_code=400, detail={
                "error_code": "SENSITIVE_CONTENT",
                "message": msg
            })
        
        # ========== 计算file_hash（用于保存到metadata）==========
        from storage.crud import calculate_file_hash
        enable_duplicate_check = os.getenv("ENABLE_DUPLICATE_CHECK", "true").lower() == "true"
        file_hash = calculate_file_hash(file_content) if enable_duplicate_check else None
        
        # ========== 正常审查流程（跳过重复检测，用户已确认）==========
        task = create_task(file.filename, len(file_content))
        await process_contract_task(task.task_id, file_content, file.filename, additional_instructions, file_hash)
        task_result = get_task(task.task_id)
        
        if task_result.status == TaskStatus.COMPLETED:
            # ========== 仅成功后才扣费 ==========
            used_bonus = use_user_bonus_credit(user_id)
            remaining_bonus = get_user_bonus_credits(user_id)

            # ========== 更新文件哈希缓存 ==========
            enable_duplicate_check = os.getenv("ENABLE_DUPLICATE_CHECK", "true").lower() == "true"
            if enable_duplicate_check:
                from storage.crud import calculate_file_hash, create_or_update_file_hash_cache
                file_hash = calculate_file_hash(file_content)
                create_or_update_file_hash_cache(user_id, file_hash, file.filename)

            return {
                "success": True,
                "message": "审查完成",
                "result": task_result.result,
                "metadata": filter_metadata_for_frontend(task_result.metadata),
                "validation": task_result.validation,
                "summary": task_result.summary,
                "record_id": task_result.record_id,
                "used_bonus": used_bonus,
                "remaining_bonus": remaining_bonus
            }
        else:
            error_msg = task_result.error or "处理失败"
            raise HTTPException(status_code=500, detail={
                "error_code": "PROCESSING_ERROR",
                "message": error_msg
            })
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理异常: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail={
            "error_code": "INTERNAL_ERROR",
            "message": f"处理失败: {str(e)}"
        })


@app.post("/api/batch/review", response_model=BatchResponse)
async def batch_review_contract(
    request: Request,
    files: List[UploadFile] = File(...),
    additional_instructions: Optional[str] = Form(""),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user_id: int = Depends(get_current_user)
):
    """批量合同审查API（需认证）- 带前置防护"""
    client_ip = request.client.host if request.client else "unknown"

    # 调试日志：打印接收到的额外审查要求
    logger.info(f"[BATCH_REVIEW] 接收到的 additional_instructions: '{additional_instructions}' (类型: {type(additional_instructions).__name__})")
    
    # ========== 前置防护0：额度检查 ==========
    remaining_bonus = get_user_bonus_credits(user_id)
    if remaining_bonus <= 0:
        raise HTTPException(status_code=403, detail={
            "error_code": "NO_CREDITS",
            "message": "您的免费额度已用完，请获取更多额度后再试"
        })
    
    # ========== 前置防护1：黑名单检查 ==========
    blacklisted = blacklist_manager.check(ip=client_ip, user_id=str(user_id))
    if blacklisted:
        raise HTTPException(status_code=403, detail={
            "error_code": "BLACKLISTED",
            "message": "账号因异常操作被临时限制，请稍后再试或联系客服解封"
        })
    auto_banned, ban_reason = is_auto_banned(ip=client_ip, user_id=user_id)
    if auto_banned:
        raise HTTPException(status_code=403, detail={
            "error_code": "AUTO_BANNED",
            "message": ban_reason
        })
    
    # ========== 前置防护2：限流检查 ==========
    rate_limiter = get_rate_limiter()
    allowed, rate_msg = rate_limiter.is_allowed(str(user_id), client_ip, limit_type="upload")
    if not allowed:
        record_violation(ip=client_ip, user_id=user_id, violation_type="rate_limit", reason=rate_msg)
        raise HTTPException(status_code=429, detail={
            "error_code": "RATE_LIMIT_EXCEEDED",
            "message": rate_msg
        })
    
    task_ids = []
    rejected_files = []

    # ========== 前置防护2.5：额外审查要求安全校验（增强版） ==========
    from utils.security import validate_extra_requirements
    from security.injection_detector import check_input_injection as enhanced_injection_check

    inj_passed, inj_error, inj_rules = enhanced_injection_check(
        additional_instructions or "", user_id=user_id, ip=client_ip
    )
    if not inj_passed:
        ban_user_for_injection(
            user_id=user_id,
            ip=client_ip,
            input_text=additional_instructions or "",
            trigger_rule=", ".join(inj_rules) if inj_rules else "injection_pattern_matched"
        )
        raise HTTPException(status_code=403, detail={
            "error_code": "INJECTION_DETECTED",
            "message": "账号已被封禁，请联系管理员"
        })

    req_valid, req_error = validate_extra_requirements(additional_instructions, user_id=user_id, ip=client_ip)
    if not req_valid:
        raise HTTPException(status_code=400, detail={
            "error_code": "INVALID_EXTRA_REQUIREMENTS",
            "message": req_error
        })

    for file in files:
        # ========== 前置防护3：基础文件校验 ==========
        valid, validation_error = validate_file_basic(file)
        if not valid:
            # 记录违规行为
            err_code = validation_error.get("error_code")
            if err_code == "INVALID_FORMAT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="format_error", reason=validation_error.get("message"))
            elif err_code == "FILE_TOO_LARGE":
                record_violation(ip=client_ip, user_id=user_id, violation_type="size_exceeded", reason=validation_error.get("message"))
            rejected_files.append(validation_error)
            continue

        # ========== 前置防护3.5：重复上传检测 ==========
        file_content = file.file.read()
        from storage.crud import calculate_file_hash, get_file_hash_cache
        enable_duplicate_check = os.getenv("ENABLE_DUPLICATE_CHECK", "true").lower() == "true"
        file_hash = None
        if enable_duplicate_check:
            file_hash = calculate_file_hash(file_content)
            existing_cache = get_file_hash_cache(user_id, file_hash)
            
            if existing_cache:
                rejected_files.append({
                    "error_code": "DUPLICATE_UPLOAD",
                    "message": f"您已上传过相同合同（{existing_cache.upload_count}次），跳过此文件",
                    "filename": file.filename,
                    "file_hash": file_hash,
                    "status_code": 409  # 使用409冲突状态码
                })
                continue

        # ========== 前置防护4：文本内容预校验 ==========
        valid, content_error, contract_text = validate_with_extractor(
            file_content,
            file.filename,
            lambda f, a: input_layer.process(f, a)
        )
        
        if not valid:
            # 记录违规行为
            err_code = content_error.get("error_code")
            if err_code == "CONTENT_TOO_SHORT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="content_too_short", reason=content_error.get("message"))
            elif err_code == "NOT_CONTRACT":
                record_violation(ip=client_ip, user_id=user_id, violation_type="not_contract", reason=content_error.get("message"))
            rejected_files.append(content_error)
            continue
        
        # ========== 前置防护5：敏感词检查 ==========
        ok, msg = check_sensitive_content(contract_text, additional_instructions)
        if not ok:
            record_violation(ip=client_ip, user_id=user_id, violation_type="sensitive_content", reason=msg)
            rejected_files.append({
                "error_code": "SENSITIVE_CONTENT",
                "message": msg,
                "filename": file.filename
            })
            continue
        
        # ========== 创建任务（仅通过校验的文件） ==========
        task = create_task(file.filename, len(file_content), user_id)
        task_ids.append(task.task_id)

        # 使用 asyncio.create_task 正确运行异步任务
        asyncio.create_task(
            process_contract_task(
                task.task_id, file_content, file.filename, additional_instructions, file_hash
            )
        )

    if len(task_ids) == 0:
        # 检查是否有重复上传的文件
        has_duplicate = any(rf.get("error_code") == "DUPLICATE_UPLOAD" for rf in rejected_files)
        if has_duplicate:
            raise HTTPException(status_code=409, detail={
                "error_code": "ALL_FILES_REJECTED",
                "message": "所有文件都是重复上传",
                "rejected_files": rejected_files
            })
        else:
            raise HTTPException(status_code=400, detail={
                "error_code": "ALL_FILES_REJECTED",
                "message": "所有文件都不符合要求",
                "rejected_files": rejected_files
            })

    result = {
        "success": True,
        "message": f"已创建 {len(task_ids)} 个审查任务",
        "task_ids": task_ids
    }

    if rejected_files:
        result["rejected_files"] = rejected_files

    return result

@app.get("/api/task/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """查询单个任务状态"""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    return {
        "task_id": task.task_id,
        "filename": task.filename,
        "file_size": task.file_size,
        "status": task.status.value,
        "progress": task.progress,
        "result": task.result,
        "error": task.error,
        "metadata": filter_metadata_for_frontend(task.metadata),  # 过滤metadata
        "validation": task.validation,
        "summary": task.summary,
        "record_id": task.record_id,
        "remaining_bonus": task.remaining_bonus
    }

@app.get("/api/task/{task_id}/stream")
async def stream_task_status(task_id: str):
    """SSE 实时任务状态推送 — 前端只需调用一次，后端主动推送进度和结果"""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    async def event_generator():
        # 1. 发送初始状态
        current_task = task
        task_data = _build_task_sse_data(current_task)
        yield _sse_event("status", task_data)
        
        # 如果任务已结束，发送结果并返回
        status = current_task.status.value if isinstance(current_task.status, TaskStatus) else str(current_task.status)
        if status in ("completed", "failed"):
            yield _sse_event("result", task_data)
            return
        
        # 2. 等待状态变更并推送
        while True:
            # 等待任务状态变更（最长 25 秒发一次心跳）
            got_update = await wait_for_task_update(task_id, timeout=25.0)
            
            current_task = get_task(task_id)
            if not current_task:
                yield _sse_event("error", {"error": "任务已删除"})
                return
            
            status = current_task.status.value if isinstance(current_task.status, TaskStatus) else str(current_task.status)
            
            if got_update:
                task_data = _build_task_sse_data(current_task)
                if status in ("completed", "failed"):
                    yield _sse_event("result", task_data)
                    return
                else:
                    yield _sse_event("progress", task_data)
            else:
                # 超时 → 发心跳保活
                yield ": keepalive\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


def _build_task_sse_data(task) -> dict:
    """构建发送给前端的任务数据字典（与 TaskResponse 一致）"""
    status = task.status.value if isinstance(task.status, TaskStatus) else str(task.status)
    return {
        "task_id": task.task_id,
        "filename": task.filename,
        "file_size": task.file_size,
        "status": status,
        "progress": task.progress,
        "result": task.result,
        "error": task.error,
        "metadata": filter_metadata_for_frontend(task.metadata),
        "validation": task.validation,
        "summary": task.summary,
        "record_id": task.record_id,
        "remaining_bonus": task.remaining_bonus,
    }


def _sse_event(event: str, data: dict) -> str:
    """构建单条 SSE 消息"""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/api/task/{task_id}/download")
async def download_report(
    task_id: str,
    format: str = "md"
):
    """下载报告文件"""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="任务未完成，无法下载")
    
    if not task.result:
        raise HTTPException(status_code=404, detail="报告内容不存在")
    
    supported_formats = ["md", "docx", "pdf"]
    if format not in supported_formats:
        raise HTTPException(status_code=400, detail=f"不支持的格式，支持: {supported_formats}")
    
    try:
        content, mime_type = output_layer.generate_report_file(
            task.result,
            format=format,
            filename=f"合同审查报告_{task.filename.rsplit('.', 1)[0]}"
        )
        
        extension_map = {
            "md": ".md",
            "docx": ".docx",
            "pdf": ".pdf"
        }
        
        filename = f"合同审查报告_{task.filename.rsplit('.', 1)[0]}{extension_map.get(format, '.md')}"
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            io.BytesIO(content),
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成文件失败: {str(e)}")

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_all_task_status():
    """查询所有任务状态"""
    tasks = get_all_tasks()
    return [
        {
            "task_id": task.task_id,
            "filename": task.filename,
            "file_size": task.file_size,
            "status": task.status.value,
            "progress": task.progress,
            "result": task.result,
            "error": task.error,
            "metadata": filter_metadata_for_frontend(task.metadata),  # 过滤metadata
            "validation": task.validation,
            "summary": task.summary
        }
        for task in tasks
    ]

@app.delete("/api/task/{task_id}")
async def delete_task(task_id: str):
    """删除任务"""
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    delete_task_func(task_id)
    return {"success": True, "message": "任务已删除"}

# ========== 下载记录报告接口 ==========
@app.get("/api/download/{record_id}")
async def download_record_report(
    record_id: int,
    format: str = "md",
    user_id: int = Depends(get_current_user)
):
    """下载记录报告文件"""
    record = get_record(record_id, user_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    if not record.get("report_markdown"):
        raise HTTPException(status_code=404, detail="报告内容不存在")
    
    supported_formats = ["md", "docx", "pdf"]
    if format not in supported_formats:
        raise HTTPException(status_code=400, detail=f"不支持的格式，支持: {supported_formats}")
    
    try:
        content, mime_type = output_layer.generate_report_file(
            record["report_markdown"],
            format=format,
            filename=f"合同审查报告_{record['filename'].rsplit('.', 1)[0]}"
        )
        
        extension_map = {
            "md": ".md",
            "docx": ".docx",
            "pdf": ".pdf"
        }
        
        filename = f"合同审查报告_{record['filename'].rsplit('.', 1)[0]}{extension_map.get(format, '.md')}"
        
        from fastapi.responses import StreamingResponse
        return StreamingResponse(
            io.BytesIO(content),
            media_type=mime_type,
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成文件失败: {str(e)}")

# ========== 管理员接口 ==========

def verify_admin(admin_token: Optional[str] = Header(None, alias="X-Admin-Token")):
    """验证管理员身份"""
    if not admin_token or admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="管理员认证失败")
    return True

@app.post("/admin/blacklist")
async def add_blacklist_item(item: BlacklistItemRequest, _: bool = Depends(verify_admin)):
    """添加黑名单条目"""
    if item.type not in ["ip", "user_id"]:
        raise HTTPException(status_code=400, detail="类型必须是 ip 或 user_id")
    
    success = add_to_blacklist(item.type, item.value, item.reason)
    if not success:
        raise HTTPException(status_code=400, detail="条目已存在")
    
    structured_logger.log_audit("BLACKLIST_ADD", details=f"添加{item.type}: {item.value}")
    return {"success": True, "message": "已添加到黑名单"}

@app.delete("/admin/blacklist")
async def remove_blacklist_item(type: str, value: str, _: bool = Depends(verify_admin)):
    """移除黑名单条目"""
    success = remove_from_blacklist(type, value)
    if not success:
        raise HTTPException(status_code=404, detail="条目不存在")
    
    structured_logger.log_audit("BLACKLIST_REMOVE", details=f"移除{type}: {value}")
    return {"success": True, "message": "已从黑名单移除"}

@app.get("/admin/blacklist")
async def list_blacklist(_: bool = Depends(verify_admin)):
    """获取所有黑名单条目"""
    items = get_all_blacklist()
    return {"success": True, "items": items}

@app.get("/admin/frequent-triggers")
async def get_frequent_triggers(days: int = 7, limit: int = 50, _: bool = Depends(verify_admin)):
    """获取高频触发词统计"""
    from security.sensitive_filter import get_frequent_triggers
    triggers = get_frequent_triggers(days=days, limit=limit)
    return {"success": True, "triggers": triggers, "days": days}

@app.get("/admin/intercept-logs")
async def get_intercept_logs(trigger_word: str = None, limit: int = 10, _: bool = Depends(verify_admin)):
    """获取拦截日志"""
    from security.sensitive_filter import get_recent_intercept_logs
    logs = get_recent_intercept_logs(trigger_word=trigger_word, limit=limit)
    return {"success": True, "logs": logs}

@app.post("/admin/add-to-whitelist")
async def add_word_to_whitelist(request: dict, _: bool = Depends(verify_admin)):
    """添加词到白名单"""
    from security.sensitive_filter import add_to_whitelist
    word = request.get("word", "").strip()
    if not word:
        raise HTTPException(status_code=400, detail="词不能为空")
    success = add_to_whitelist(word)
    if success:
        structured_logger.log_audit("WHITELIST_ADD", details=f"添加白名单词: {word}")
        return {"success": True, "message": f"已将 '{word}' 添加到白名单"}
    raise HTTPException(status_code=500, detail="添加失败")

@app.post("/admin/remove-from-whitelist")
async def remove_word_from_whitelist(request: dict, _: bool = Depends(verify_admin)):
    """从白名单移除词"""
    from security.sensitive_filter import remove_from_whitelist
    word = request.get("word", "").strip()
    if not word:
        raise HTTPException(status_code=400, detail="词不能为空")
    success = remove_from_whitelist(word)
    if success:
        structured_logger.log_audit("WHITELIST_REMOVE", details=f"移除白名单词: {word}")
        return {"success": True, "message": f"已将 '{word}' 从白名单移除"}
    raise HTTPException(status_code=404, detail="词不在白名单中")

@app.get("/admin/whitelist")
async def get_whitelist(_: bool = Depends(verify_admin)):
    """获取当前白名单"""
    from security.sensitive_filter import WHITELIST
    return {"success": True, "whitelist": sorted(WHITELIST)}

@app.get("/admin/malicious-stats")
async def get_malicious_stats(
    identifier: Optional[str] = None,
    _: bool = Depends(verify_admin)
):
    """获取恶意行为统计"""
    tracker = get_malicious_tracker()
    
    if identifier:
        # 查看特定标识符的统计
        stats = tracker.get_violation_stats(identifier)
        banned, reason = tracker.is_auto_banned(identifier)
        return {
            "success": True,
            "identifier": identifier,
            "stats": stats,
            "is_banned": banned,
            "ban_reason": reason if banned else None
        }
    else:
        # 返回通用信息
        return {
            "success": True,
            "message": "请提供 identifier 参数查看特定统计",
            "threshold": tracker._threshold,
            "ban_duration": tracker._ban_duration
        }

@app.get("/admin/dashboard")
async def get_admin_dashboard(_: bool = Depends(verify_admin)):
    """管理后台HTML页面"""
    from security.sensitive_filter import get_frequent_triggers, get_recent_intercept_logs, WHITELIST
    from monitoring import get_metrics_summary
    whitelist_count = len(WHITELIST)
    metrics = get_metrics_summary()
    return HTMLResponse(content="""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SageAI 安全监控后台</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 { color: #333; margin-bottom: 20px; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { color: #666; font-size: 16px; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { text-align: left; padding: 12px; border-bottom: 1px solid #eee; }
        th { background: #fafafa; color: #666; font-weight: 500; }
        .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
        .badge-warning { background: #fff3cd; color: #856404; }
        .btn { padding: 6px 12px; border: none; border-radius: 4px; cursor: pointer; font-size: 12px; }
        .btn-primary { background: #007bff; color: white; }
        .btn-success { background: #28a745; color: white; }
        .btn:hover { opacity: 0.8; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .stat-item { background: #f8f9fa; padding: 15px; border-radius: 6px; text-align: center; }
        .stat-value { font-size: 28px; font-weight: bold; color: #007bff; }
        .stat-label { color: #666; font-size: 14px; margin-top: 5px; }
        .text-preview { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: #666; font-size: 12px; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; }
        .modal.active { display: flex; align-items: center; justify-content: center; }
        .modal-content { background: white; padding: 20px; border-radius: 8px; max-width: 600px; max-height: 80vh; overflow-y: auto; width: 90%; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
        .modal-close { background: none; border: none; font-size: 24px; cursor: pointer; }
        .log-item { background: #f8f9fa; padding: 10px; margin-bottom: 10px; border-radius: 4px; font-size: 13px; }
        .log-item .meta { color: #666; margin-bottom: 5px; }
        .log-item .content { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>SageAI 安全监控后台</h1>
        <div class="card">
            <h2>统计数据（近7天）</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="total-count">-</div>
                    <div class="stat-label">总拦截次数</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="unique-words">-</div>
                    <div class="stat-label">触发词数量</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="whitelist-count">""" + str(whitelist_count) + """</div>
                    <div class="stat-label">白名单词数</div>
                </div>
            </div>
        </div>
        <div class="card">
            <h2>高频触发词排行</h2>
            <table>
                <thead>
                    <tr><th>排名</th><th>触发词</th><th>次数</th><th>最近时间</th><th>操作</th></tr>
                </thead>
                <tbody id="triggers-table"><tr><td colspan="5">加载中...</td></tr></tbody>
            </table>
        </div>
        <div class="card">
            <h2>最近拦截日志</h2>
            <div id="recent-logs"><div class="log-item">加载中...</div></div>
        </div>
    </div>
    <div class="modal" id="logs-modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 id="modal-title">拦截样本</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div id="modal-body"></div>
        </div>
    </div>
    <script>
        const TOKEN = localStorage.getItem('admin_token') || prompt('请输入管理员Token:');
        if (!TOKEN) location.href = '/login';
        async function api(url) {
            const r = await fetch(url, { headers: { 'X-Admin-Token': TOKEN } });
            if (r.status === 401) { alert('Token无效'); location.href = '/login'; }
            return r.json();
        }
        async function load() {
            const d = await api('/admin/frequent-triggers?days=7&limit=20');
            if (d.success) {
                renderT(d.triggers);
                document.getElementById('total-count').textContent = d.triggers.reduce((s, t) => s + t.count, 0);
                document.getElementById('unique-words').textContent = d.triggers.length;
            }
            const l = await api('/admin/intercept-logs?limit=5');
            if (l.success) renderL(l.logs);
        }
        function renderT(triggers) {
            const tb = document.getElementById('triggers-table');
            if (!triggers.length) { tb.innerHTML = '<tr><td colspan="5">暂无数据</td></tr>'; return; }
            tb.innerHTML = triggers.map((t, i) => '<tr><td>' + (i+1) + '</td><td><span class="badge badge-warning">' + t.word + '</span></td><td><strong>' + t.count + '</strong></td><td>' + new Date(t.last_trigger_time).toLocaleString() + '</td><td><button class="btn btn-primary" onclick="show(\'' + t.word + '\')">样本</button> <button class="btn btn-success" onclick="addW(\'' + t.word + '\')">白名单</button></td></tr>').join('');
        }
        function renderL(logs) {
            const div = document.getElementById('recent-logs');
            if (!logs.length) { div.innerHTML = '<div class="log-item">暂无数据</div>'; return; }
            div.innerHTML = logs.map(l => '<div class="log-item"><div class="meta">' + new Date(l.timestamp).toLocaleString() + ' | IP:' + l.ip + ' | ' + l.trigger_word + '</div><div class="content text-preview">' + (l.text_preview || '(无)') + '</div></div>').join('');
        }
        async function show(word) {
            const d = await api('/admin/intercept-logs?trigger_word=' + encodeURIComponent(word) + '&limit=10');
            if (!d.success) return;
            document.getElementById('modal-title').textContent = '触发词: ' + word;
            document.getElementById('modal-body').innerHTML = d.logs.map(l => '<div class="log-item"><div class="meta">' + new Date(l.timestamp).toLocaleString() + ' | IP:' + l.ip + ' | User:' + (l.user_id || '匿名') + '</div><div class="content">' + (l.text_preview || '(无)') + '</div></div>').join('') || '<p>暂无样本</p>';
            document.getElementById('logs-modal').classList.add('active');
        }
        function closeModal() { document.getElementById('logs-modal').classList.remove('active'); }
        async function addW(word) {
            if (!confirm('确定将 "' + word + '" 加入白名单？')) return;
            const r = await fetch('/admin/add-to-whitelist', { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Admin-Token': TOKEN }, body: JSON.stringify({ word }) });
            const d = await r.json();
            if (d.success) { alert(d.message); load(); }
            else alert('操作失败');
        }
        load();
    </script>
</body>
</html>""")

# ========== 监控接口 ==========

@app.get("/health")
async def health_check_root():
    """健康检查接口（根路径，供Docker健康检查使用）- 不依赖psutil"""
    import time as _time
    from datetime import datetime as _dt
    uptime = int(_time.time() - _time.time())  # simplified
    return {
        "status": "healthy",
        "timestamp": _dt.now().isoformat(),
        "uptime": "running",
        "system": {"status": "ok"}
    }

@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    from monitoring import get_health_status
    return get_health_status()

@app.get("/api/metrics")
async def get_metrics():
    """获取服务指标"""
    from monitoring import get_metrics_summary
    return {"success": True, "data": get_metrics_summary()}

@app.get("/api/metrics/endpoints")
async def get_endpoint_metrics():
    """获取端点级别的指标"""
    from monitoring import get_endpoint_metrics
    return {"success": True, "data": get_endpoint_metrics()}

@app.post("/api/metrics/reset")
async def reset_all_metrics(_: bool = Depends(verify_admin)):
    """重置所有指标（管理员）"""
    from monitoring import reset_metrics
    reset_metrics()
    return {"success": True, "message": "指标已重置"}

# ========== 隐私政策与用户协议 ==========

@app.get("/privacy")
async def get_privacy_policy():
    """隐私政策页面"""
    return {
        "title": "SageAI 隐私政策",
        "content": """
# SageAI 隐私政策

## 一、我们收集的信息
1. **账号信息**：手机号（用于登录和身份验证）
2. **临时数据**：您上传的合同文件内容仅在审查过程中临时存储在内存中，审查完成后立即丢弃，不会保存到磁盘或数据库
3. **操作记录**：您的审查操作记录（不含合同内容）

## 二、数据使用
我们收集的信息仅用于：
- 提供合同审查服务
- 账户安全管理
- 服务改进（不含合同内容）

## 三、数据共享
我们不会向任何第三方共享您的合同内容或个人身份信息，除非：
- 获得您的明确同意
- 法律法规要求

## 四、您的权利
1. **删除账户**：您可以请求删除您的账户及所有相关数据
2. **删除记录**：您可以随时删除您的审查记录
3. **查询数据**：您可以查询我们保存的您的相关信息

## 五、免责声明
AI生成的审查报告仅供参考，不构成正式法律意见。我们建议您就重要法律事务咨询执业律师。
        """
    }

@app.get("/terms")
async def get_terms_of_service():
    """用户协议页面"""
    return {
        "title": "SageAI 用户服务协议",
        "content": """
# SageAI 用户服务协议

## 一、服务说明
SageAI 是一款基于人工智能的合同审查辅助工具，提供合同文本的分析和风险提示功能。

## 二、用户承诺
1. 您承诺上传的文件不包含违法内容或敏感信息
2. 您承诺遵守相关法律法规，不将本服务用于非法用途
3. 您理解AI分析结果仅供参考，不替代专业法律意见

## 三、免责声明
1. 本服务不提供正式法律意见，如有重要法律事务请咨询执业律师
2. 我们不对AI分析结果的准确性或完整性作任何保证
3. 我们不对因使用本服务造成的任何损失承担责任

## 四、服务变更
我们保留随时修改或终止服务的权利。
        """
    }

# ========== 熔断器状态接口 ==========

@app.get("/api/circuit-breaker")
async def get_circuit_breaker_status_endpoint():
    """获取熔断器状态（供监控使用）"""
    status = get_circuit_breaker_status()
    return {
        "success": True,
        "state": status["state"],
        "failure_count": status["failure_count"],
        "threshold": status["threshold"],
        "timeout_seconds": status["timeout"]
    }

# ========== 隐私政策与用户协议 ==========

@app.get("/privacy")
async def get_privacy_policy():
    """隐私政策页面"""
    return {
        "title": "SageAI 隐私政策",
        "content": """
# SageAI 隐私政策

## 一、我们收集的信息
1. **账号信息**：手机号（用于登录和身份验证）
2. **临时数据**：您上传的合同文件内容仅在审查过程中临时存储在内存中，审查完成后立即丢弃，不会保存到磁盘或数据库
3. **操作记录**：您的审查操作记录（不含合同内容）

## 二、数据使用
我们收集的信息仅用于：
- 提供合同审查服务
- 账户安全管理
- 服务改进（不含合同内容）

## 三、数据共享
我们不会向任何第三方共享您的合同内容或个人身份信息，除非：
- 获得您的明确同意
- 法律法规要求

## 四、您的权利
1. **删除账户**：您可以请求删除您的账户及所有相关数据
2. **删除记录**：您可以随时删除您的审查记录
3. **查询数据**：您可以查询我们保存的您的相关信息

## 五、免责声明
AI生成的审查报告仅供参考，不构成正式法律意见。我们建议您就重要法律事务咨询执业律师。
        """
    }

@app.get("/terms")
async def get_terms_of_service():
    """用户协议页面"""
    return {
        "title": "SageAI 用户服务协议",
        "content": """
# SageAI 用户服务协议

## 一、服务说明
SageAI 是一款基于人工智能的合同审查辅助工具，提供合同文本的分析和风险提示功能。

## 二、用户承诺
1. 您承诺上传的文件不包含违法内容或敏感信息
2. 您承诺遵守相关法律法规，不将本服务用于非法用途
3. 您理解AI分析结果仅供参考，不替代专业法律意见

## 三、免责声明
1. 本服务不提供正式法律意见，如有重要法律事务请咨询执业律师
2. 我们不对AI分析结果的准确性或完整性作任何保证
3. 我们不对因使用本服务造成的任何损失承担责任

## 四、服务变更
我们保留随时修改或终止服务的权利。
        """
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8016)
