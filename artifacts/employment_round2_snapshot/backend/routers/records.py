"""报告记录相关路由"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from auth.routes import get_current_user
from storage.crud import get_records_by_user, get_record, delete_record

router = APIRouter(prefix="/api/records", tags=["records"])


class RecordListItem(BaseModel):
    """记录列表项"""
    id: int
    filename: str
    created_at: str
    metadata: Optional[dict] = None  # 添加metadata字段


class RecordDetail(BaseModel):
    """记录详情"""
    id: int
    filename: str
    report_markdown: str
    metadata: Optional[dict]
    created_at: str
    updated_at: str


def format_datetime(dt):
    """格式化datetime为带时区信息的字符串"""
    if hasattr(dt, 'isoformat'):
        # 如果是带时区的datetime，直接返回isoformat
        result = dt.isoformat()
        # 如果结果不包含时区信息，添加Z表示UTC
        if '+' not in result and 'Z' not in result:
            result += 'Z'
        return result
    return str(dt)


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


@router.get("", response_model=List[RecordListItem])
async def get_user_records(user_id: int = Depends(get_current_user)):
    """获取当前用户的所有历史报告列表（不含报告全文）"""
    records = get_records_by_user(user_id)
    return [
        {
            "id": r["id"],
            "filename": r["filename"],
            "created_at": format_datetime(r["created_at"]),
            "metadata": filter_metadata_for_frontend(r.get("metadata"))  # 过滤metadata
        }
        for r in records
    ]


@router.get("/{record_id}", response_model=RecordDetail)
async def get_record_detail(record_id: int, user_id: int = Depends(get_current_user)):
    """获取指定报告的完整内容"""
    record = get_record(record_id, user_id)
    
    if not record:
        raise HTTPException(status_code=404, detail="报告不存在或无权访问")
    
    return {
        "id": record["id"],
        "filename": record["filename"],
        "report_markdown": record["report_markdown"],
        "metadata": filter_metadata_for_frontend(record["metadata"]),  # 过滤metadata
        "created_at": format_datetime(record["created_at"]),
        "updated_at": format_datetime(record["updated_at"])
    }


@router.delete("/{record_id}")
async def delete_record_by_id(record_id: int, user_id: int = Depends(get_current_user)):
    """删除指定记录（只能删除自己的报告）"""
    success = delete_record(record_id, user_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="报告不存在或无权删除")
    
    return {"message": "删除成功"}
