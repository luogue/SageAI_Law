"""数据库模型"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from .database import Base, CHINA_TZ


class User(Base):
    """用户表"""
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    bonus_credits = Column(Integer, default=0, nullable=False)  # 免费赠送的审查额度
    free_review_quota = Column(Integer, default=0, nullable=False)  # 免费审查额度（历史字段）
    invited_by = Column(Integer, ForeignKey("user.id"))  # 邀请人ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Record(Base):
    """审查记录表 - 不保存原始合同文本"""
    __tablename__ = "record"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    filename = Column(String, nullable=False)  # 仅保存文件名
    report_markdown = Column(Text)
    metadata_json = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Feedback(Base):
    """用户反馈表"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    report_id = Column(String(50), nullable=False)  # 关联的报告ID（随机生成）
    feedback_type = Column(String(20), nullable=False)  # "useful" 或 "not_useful" 或 "detailed"
    categories = Column(Text)  # JSON格式存储的问题分类
    comment = Column(Text)  # 用户填写的文字反馈
    upload_consent = Column(Boolean, default=False, nullable=False)  # 是否同意上传合同文本
    contract_text = Column(Text)  # 用户主动上传的合同文本（脱敏存储，仅在upload_consent为True时存储）
    contract_hash = Column(String(64))  # 合同文本的哈希值，用于去重
    # 质量评分字段
    quality_score = Column(Integer, default=0, nullable=False)  # AI评分（0-100）
    suggested_bonus = Column(Integer, default=0, nullable=False)  # 建议奖励额度
    ai_reason = Column(Text)  # AI评分理由
    # 审核相关字段
    bonus_awarded = Column(Integer, default=0, nullable=False)  # 实际赠送的额度
    status = Column(String(20), default="pending", nullable=False)  # 状态：pending/approved/rejected
    reviewed_at = Column(DateTime(timezone=True))  # 审核时间
    reviewer_id = Column(Integer, ForeignKey("user.id"))  # 审核人ID
    reviewed_by = Column(String(50))  # 审核人用户名
    reject_reason = Column(Text)  # 驳回原因（可选）
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BonusLog(Base):
    """额度赠送记录表（用于每日限额和去重）"""
    __tablename__ = "bonus_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    bonus_type = Column(String(50), nullable=False)  # "feedback" 或 "contract_upload"
    contract_hash = Column(String(64))  # 用于合同去重（如果是合同上传）
    awarded_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RewardLog(Base):
    """奖励发放记录表 - 记录每次奖励发放详情"""
    __tablename__ = "reward_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # 发放额度
    reason = Column(String(50), nullable=False)  # 发放原因，如 "feedback_approve"
    related_feedback_id = Column(Integer, ForeignKey("feedback.id"))  # 关联的反馈ID
    operator = Column(String(50))  # 操作管理员
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InviteReward(Base):
    """邀请奖励发放记录表"""
    __tablename__ = "invite_rewards"
    
    id = Column(Integer, primary_key=True, index=True)
    inviter_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # 邀请人ID
    invitee_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # 被邀请人ID
    reward_credits = Column(Integer, nullable=False)  # 奖励额度
    status = Column(String(20), default="pending", nullable=False)  # 状态：pending/completed/expired
    invitee_first_review_at = Column(DateTime(timezone=True))  # 被邀请人首次完成审查的时间
    reward_granted_at = Column(DateTime(timezone=True))  # 奖励发放时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Blacklist(Base):
    """黑名单表"""
    __tablename__ = "blacklist"
    
    id = Column(Integer, primary_key=True, index=True)
    blacklist_type = Column(String, nullable=False)  # 'ip' 或 'user_id'
    value = Column(String, nullable=False, unique=True, index=True)
    reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InterceptLog(Base):
    """拦截日志表"""
    __tablename__ = "intercept_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    user_id = Column(Integer, nullable=True)
    ip = Column(String(45), nullable=False, index=True)
    request_path = Column(String(100), nullable=False)
    trigger_type = Column(String(50), nullable=False)  # sensitive_word, cloud_green, length
    trigger_word = Column(String(200), nullable=False)
    text_preview = Column(Text, nullable=True)
    action = Column(String(20), nullable=False, default="rejected")


class FileHashCache(Base):
    """文件哈希缓存表 - 用于检测重复上传"""
    __tablename__ = "file_hash_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    file_hash = Column(String(64), nullable=False, index=True)  # MD5哈希值
    filename = Column(String, nullable=True)  # 原始文件名
    first_upload_time = Column(DateTime(timezone=True), server_default=func.now())
    last_upload_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    upload_count = Column(Integer, default=1, nullable=False)  # 上传次数
    
    __table_args__ = (
        # 同一用户的同一文件哈希唯一
        {'extend_existing': True},
    )


class TaskRecord(Base):
    """任务状态持久化表 - 防止容器重启后任务丢失"""
    __tablename__ = "task_record"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    filename = Column(String, nullable=False)
    file_size = Column(Integer, default=0)
    status = Column(String(20), default="pending", nullable=False)  # pending/uploading/processing/completed/failed
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    remaining_bonus = Column(Integer, nullable=True)
    record_id = Column(Integer, nullable=True)
    progress = Column(Integer, default=0)
    result = Column(Text, nullable=True)
    error = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)   # JSON 序列化的 metadata
    validation_json = Column(Text, nullable=True)  # JSON 序列化的 validation
    summary_json = Column(Text, nullable=True)     # JSON 序列化的 summary
    trace_id = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
