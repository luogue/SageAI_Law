"""CRUD操作 - 不保存原始合同文本"""
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import User, Record, Blacklist, Feedback, BonusLog, RewardLog, InviteReward, FileHashCache, AdminLog, SecurityEvent, Admin
from .database import get_db, engine, Base


def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)


def parse_phone_number(phone: str) -> tuple:
    """
    解析手机号，分离区号和手机号
    :return: (country_code, mobile) 元组
    """
    # 提取纯数字
    phone_digits = ''.join(filter(str.isdigit, phone))
    
    # 默认区号
    country_code = "+86"
    
    # 处理带区号的情况
    if phone.startswith('+'):
        # 找到第一个数字的位置
        for i, char in enumerate(phone):
            if char.isdigit():
                # 尝试解析区号
                if phone[i:i+2] == '86':  # +86
                    country_code = '+86'
                    phone_digits = phone_digits[2:]
                elif phone[i] == '1':  # +1 (USA)
                    country_code = '+1'
                    phone_digits = phone_digits[1:]
                else:
                    # 默认中国区号
                    country_code = '+86'
                break
    
    # 如果是中国手机号且长度为11位，直接使用
    if len(phone_digits) == 11 and phone_digits.startswith('1'):
        return country_code, phone_digits
    
    return country_code, phone_digits


def create_user(mobile: str, password_hash: str, country_code: str = "+86") -> User:
    """创建用户"""
    db = next(get_db())
    user = User(country_code=country_code, mobile=mobile, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_mobile(mobile: str, country_code: str = None) -> User:
    """根据手机号获取用户（支持纯手机号或带区号的手机号）"""
    db = next(get_db())
    
    # 如果提供了区号，精确查询
    if country_code:
        return db.query(User).filter(
            User.mobile == mobile,
            User.country_code == country_code
        ).first()
    
    # 否则只按手机号查询（兼容旧数据）
    return db.query(User).filter(User.mobile == mobile).first()


def get_user_by_id(user_id: int) -> User:
    """根据ID获取用户"""
    db = next(get_db())
    return db.query(User).filter(User.id == user_id).first()


def update_user_password(mobile: str, new_password_hash: str) -> bool:
    """根据手机号重置密码，返回是否成功"""
    db = next(get_db())
    user = db.query(User).filter(User.mobile == mobile).first()
    if not user:
        # 尝试去掉国际区号查询
        phone_digits = ''.join(filter(str.isdigit, mobile))
        user = db.query(User).filter(User.mobile == phone_digits).first()
    if user:
        user.password_hash = new_password_hash
        db.commit()
        return True
    return False


def create_record(user_id: int, filename: str, report_md: str, metadata: dict, raw_output: str = None) -> int:
    """创建记录 - 不保存原始合同文件"""
    db = next(get_db())
    
    record = Record(
        user_id=user_id,
        filename=filename,
        report_markdown=report_md,
        raw_output=raw_output,
        metadata_json=json.dumps(metadata) if metadata else None
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return record.id


def get_records_by_user(user_id: int) -> list:
    """获取用户的所有记录"""
    db = next(get_db())
    records = db.query(Record).filter(Record.user_id == user_id).order_by(Record.created_at.desc()).all()
    result = []
    for r in records:
        metadata = json.loads(r.metadata_json) if r.metadata_json else None
        result.append({
            "id": r.id,
            "filename": r.filename,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "metadata": metadata  # 添加 metadata 字段，包含 file_hash
        })
    return result


def get_record(record_id: int, user_id: int) -> dict:
    """获取单条记录详情"""
    db = next(get_db())
    record = db.query(Record).filter(Record.id == record_id, Record.user_id == user_id).first()
    
    if not record:
        return None
    
    metadata = json.loads(record.metadata_json) if record.metadata_json else None
    
    return {
        "id": record.id,
        "filename": record.filename,
        "report_markdown": record.report_markdown,
        "metadata": metadata,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "updated_at": record.updated_at.isoformat() if record.updated_at else None
    }


def delete_record(record_id: int, user_id: int) -> bool:
    """删除记录"""
    db = next(get_db())
    record = db.query(Record).filter(Record.id == record_id, Record.user_id == user_id).first()
    
    if not record:
        return False
    
    db.delete(record)
    db.commit()
    
    return True


# ========== 黑名单管理 ==========

def add_to_blacklist(blacklist_type: str, value: str, reason: str = "") -> bool:
    """添加到黑名单"""
    db = next(get_db())
    try:
        existing = db.query(Blacklist).filter(
            Blacklist.blacklist_type == blacklist_type,
            Blacklist.value == value
        ).first()
        if existing:
            existing.reason = reason or existing.reason
            db.commit()
            return True
        item = Blacklist(blacklist_type=blacklist_type, value=value, reason=reason)
        db.add(item)
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        return False


def remove_from_blacklist(blacklist_type: str, value: str) -> bool:
    """从黑名单移除"""
    db = next(get_db())
    item = db.query(Blacklist).filter(
        Blacklist.blacklist_type == blacklist_type,
        Blacklist.value == value
    ).first()
    
    if item:
        db.delete(item)
        db.commit()
        return True
    return False


def is_in_blacklist(blacklist_type: str, value: str) -> bool:
    """检查是否在黑名单"""
    db = next(get_db())
    return db.query(Blacklist).filter(
        Blacklist.blacklist_type == blacklist_type,
        Blacklist.value == value
    ).first() is not None


def get_all_blacklist() -> list:
    """获取所有黑名单条目"""
    db = next(get_db())
    items = db.query(Blacklist).order_by(Blacklist.created_at.desc()).all()
    return [
        {
            "id": i.id,
            "blacklist_type": i.blacklist_type,
            "value": i.value,
            "reason": i.reason,
            "created_at": i.created_at.isoformat() if i.created_at else None
        }
        for i in items
    ]


def check_blacklist(ip: str = None, user_id: str = None) -> str | None:
    """检查IP或用户ID是否在黑名单，返回被拦截的类型"""
    if ip and is_in_blacklist("ip", ip):
        return "ip"
    if user_id and is_in_blacklist("user_id", str(user_id)):
        return "user_id"
    return None


# ========== 用户额度管理 ==========

def get_user_bonus_credits(user_id: int) -> int:
    """获取用户剩余免费额度"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    return user.bonus_credits if user else 0


def add_user_bonus_credits(user_id: int, amount: int) -> int:
    """增加用户免费额度，返回当前剩余额度"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.bonus_credits += amount
        db.commit()
        db.refresh(user)
        return user.bonus_credits
    return 0


def use_user_bonus_credit(user_id: int) -> bool:
    """使用1次免费额度，返回是否成功"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    if user and user.bonus_credits > 0:
        user.bonus_credits -= 1
        db.commit()
        return True
    return False


# ========== 每日限额管理 ==========

def get_today_bonus_count(user_id: int) -> int:
    """获取用户今日已获得的额度赠送次数"""
    db = next(get_db())
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(BonusLog).filter(
        BonusLog.user_id == user_id,
        BonusLog.created_at >= today_start
    ).count()


def check_contract_hash_exists(contract_hash: str, days: int = 7) -> bool:
    """检查合同哈希是否在指定天数内已存在（用于去重）"""
    db = next(get_db())
    cutoff_date = datetime.now() - timedelta(days=days)
    exists = db.query(BonusLog).filter(
        BonusLog.contract_hash == contract_hash,
        BonusLog.created_at >= cutoff_date
    ).first() is not None
    return exists


def compute_contract_hash(contract_text: str) -> str:
    """计算合同文本的哈希值"""
    return hashlib.sha256(contract_text.encode('utf-8')).hexdigest()


def add_bonus_log(user_id: int, bonus_type: str, awarded_amount: int, contract_hash: str = None) -> None:
    """记录额度赠送"""
    db = next(get_db())
    log = BonusLog(
        user_id=user_id,
        bonus_type=bonus_type,
        awarded_amount=awarded_amount,
        contract_hash=contract_hash
    )
    db.add(log)
    db.commit()


# ========== 反馈管理 ==========

def create_feedback(
    user_id: int,
    report_id: str,
    feedback_type: str,
    categories: list,
    comment: str,
    upload_consent: bool,
    contract_text: str = None,
    quality_score: int = 0,
    suggested_bonus: int = 0,
    ai_reason: str = None
) -> Feedback:
    """创建用户反馈"""
    db = next(get_db())
    
    contract_hash = None
    if upload_consent and contract_text:
        contract_hash = compute_contract_hash(contract_text)
    
    feedback = Feedback(
        user_id=user_id,
        report_id=report_id,
        feedback_type=feedback_type,
        categories=json.dumps(categories) if categories else None,
        comment=comment,
        upload_consent=upload_consent,
        contract_text=contract_text if upload_consent else None,
        contract_hash=contract_hash,
        quality_score=quality_score,
        suggested_bonus=suggested_bonus,
        ai_reason=ai_reason
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    return feedback


def update_feedback_bonus(feedback_id: int, bonus_awarded: int) -> None:
    """更新反馈的赠送额度"""
    db = next(get_db())
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback:
        feedback.bonus_awarded = bonus_awarded
        db.commit()


def get_feedback_by_id(feedback_id: int) -> Optional[Feedback]:
    """根据ID获取反馈"""
    db = next(get_db())
    return db.query(Feedback).filter(Feedback.id == feedback_id).first()


def update_feedback_status(
    feedback_id: int,
    status: str,
    reviewed_at: datetime,
    bonus_awarded: int = 0,
    reject_reason: Optional[str] = None,
    reviewed_by: Optional[str] = None
) -> None:
    """更新反馈审核状态"""
    db = next(get_db())
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback:
        feedback.status = status
        feedback.reviewed_at = reviewed_at
        feedback.bonus_awarded = bonus_awarded
        feedback.reject_reason = reject_reason
        feedback.reviewed_by = reviewed_by
        db.commit()


def update_feedback_score(
    feedback_id: int,
    quality_score: int,
    suggested_bonus: int,
    ai_reason: str
) -> None:
    """更新反馈AI评分"""
    db = next(get_db())
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if feedback:
        feedback.quality_score = quality_score
        feedback.suggested_bonus = suggested_bonus
        feedback.ai_reason = ai_reason
        db.commit()


def get_feedbacks(
    page: int = 1,
    limit: int = 20,
    category: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = None
) -> List[dict]:
    """获取反馈列表（管理员接口）"""
    db = next(get_db())
    
    # 设置排序方式
    if sort_by == "quality_score":
        query = db.query(Feedback).order_by(Feedback.quality_score.desc())
    else:
        query = db.query(Feedback).order_by(Feedback.created_at.desc())
    
    if category:
        query = query.filter(Feedback.categories.like(f'%"{category}"%'))
    
    if status:
        query = query.filter(Feedback.status == status)
    
    offset = (page - 1) * limit
    feedbacks = query.offset(offset).limit(limit).all()
    
    result = []
    for f in feedbacks:
        categories = json.loads(f.categories) if f.categories else None
        # 脱敏合同文本（只展示前100个字符）
        contract_preview = None
        if f.contract_text and len(f.contract_text) > 100:
            contract_preview = f.contract_text[:100] + "..."
        elif f.contract_text:
            contract_preview = f.contract_text
            
        result.append({
            "id": f.id,
            "user_id": f.user_id,
            "report_id": f.report_id,
            "feedback_type": f.feedback_type,
            "categories": categories,
            "comment": f.comment,
            "upload_consent": f.upload_consent,
            "contract_preview": contract_preview,
            "quality_score": f.quality_score,
            "suggested_bonus": f.suggested_bonus,
            "ai_reason": f.ai_reason,
            "bonus_awarded": f.bonus_awarded,
            "status": f.status,
            "reviewed_at": f.reviewed_at.isoformat() if f.reviewed_at else None,
            "reviewed_by": f.reviewed_by,
            "reject_reason": f.reject_reason,
            "created_at": f.created_at.isoformat() if f.created_at else None
        })
    return result


def get_feedback_count(category: Optional[str] = None, status: Optional[str] = None) -> int:
    """获取反馈总数"""
    db = next(get_db())
    query = db.query(Feedback)
    if category:
        query = query.filter(Feedback.categories.like(f'%"{category}"%'))
    if status:
        query = query.filter(Feedback.status == status)
    return query.count()


def check_feedback_contract_uploaded(report_id: str, user_id: int) -> bool:
    """检查该用户是否已为同一报告上传过合同"""
    db = next(get_db())
    exists = db.query(Feedback).filter(
        Feedback.report_id == report_id,
        Feedback.user_id == user_id,
        Feedback.upload_consent == True
    ).first() is not None
    return exists


# ========== 奖励发放记录管理 ==========

def create_reward_log(
    user_id: int,
    amount: int,
    reason: str,
    related_feedback_id: int = None,
    operator: str = None
) -> RewardLog:
    """创建奖励发放记录"""
    db = next(get_db())
    log = RewardLog(
        user_id=user_id,
        amount=amount,
        reason=reason,
        related_feedback_id=related_feedback_id,
        operator=operator
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_reward_logs(
    user_id: int = None,
    feedback_id: int = None,
    page: int = 1,
    limit: int = 20
) -> List[dict]:
    """获取奖励发放记录列表"""
    db = next(get_db())
    query = db.query(RewardLog).order_by(RewardLog.created_at.desc())
    
    if user_id:
        query = query.filter(RewardLog.user_id == user_id)
    if feedback_id:
        query = query.filter(RewardLog.related_feedback_id == feedback_id)
    
    offset = (page - 1) * limit
    logs = query.offset(offset).limit(limit).all()
    
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "amount": log.amount,
            "reason": log.reason,
            "related_feedback_id": log.related_feedback_id,
            "operator": log.operator,
            "created_at": log.created_at.isoformat() if log.created_at else None
        }
        for log in logs
    ]


def get_reward_log_count(user_id: int = None) -> int:
    """获取奖励发放记录总数"""
    db = next(get_db())
    query = db.query(RewardLog)
    if user_id:
        query = query.filter(RewardLog.user_id == user_id)
    return query.count()


def get_total_reward_amount(user_id: int = None) -> int:
    """获取奖励发放总额"""
    db = next(get_db())
    query = db.query(RewardLog)
    if user_id:
        query = query.filter(RewardLog.user_id == user_id)
    
    total = query.with_entities(RewardLog.amount).all()
    return sum([row[0] for row in total])


# ========== 邀请奖励管理 ==========

def create_user_with_invite(mobile: str, password_hash: str, inviter_id: int = None, country_code: str = "+86") -> User:
    """创建用户（支持邀请人）"""
    db = next(get_db())
    user = User(country_code=country_code, mobile=mobile, password_hash=password_hash, invited_by=inviter_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_invite_reward(inviter_id: int, invitee_id: int, reward_credits: int, status: str = "pending") -> InviteReward:
    """创建邀请奖励记录"""
    db = next(get_db())
    reward = InviteReward(
        inviter_id=inviter_id,
        invitee_id=invitee_id,
        reward_credits=reward_credits,
        status=status
    )
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


def get_invite_reward_by_invitee(invitee_id: int) -> Optional[InviteReward]:
    """根据被邀请人ID获取邀请奖励记录"""
    db = next(get_db())
    return db.query(InviteReward).filter(InviteReward.invitee_id == invitee_id).first()


# ========== 管理员账号管理 ==========

def get_admin_by_username(username: str) -> Optional[Admin]:
    """根据用户名获取管理员"""
    db = next(get_db())
    return db.query(Admin).filter(Admin.username == username).first()


def create_admin(username: str, password_hash: str) -> Admin:
    """创建管理员账号"""
    db = next(get_db())
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def verify_admin_password(username: str, password_hash: str) -> bool:
    """验证管理员密码，返回是否验证成功"""
    admin = get_admin_by_username(username)
    if not admin:
        return False
    return admin.password_hash == password_hash


def get_invite_reward_by_inviter_and_invitee(inviter_id: int, invitee_id: int) -> Optional[InviteReward]:
    """根据邀请人和被邀请人ID获取邀请奖励记录"""
    db = next(get_db())
    return db.query(InviteReward).filter(
        InviteReward.inviter_id == inviter_id,
        InviteReward.invitee_id == invitee_id
    ).first()


def update_invite_reward_status(reward_id: int, status: str) -> None:
    """更新邀请奖励状态"""
    db = next(get_db())
    reward = db.query(InviteReward).filter(InviteReward.id == reward_id).first()
    if reward:
        reward.status = status
        db.commit()


def check_phone_has_been_invited(mobile: str) -> bool:
    """检查手机号是否已作为被邀请人注册过"""
    db = next(get_db())
    user = db.query(User).filter(User.mobile == mobile).first()
    if user and user.invited_by is not None:
        return True
    return False


def get_invitee_count_by_ip(ip: str, hours: int = 24) -> int:
    """获取指定IP在指定时间内注册的被邀请人数"""
    db = next(get_db())
    cutoff_date = datetime.now() - timedelta(hours=hours)
    count = db.query(User).filter(
        User.invited_by.isnot(None),
        User.created_at >= cutoff_date
    ).count()
    return count


def get_invite_rewards_by_inviter(inviter_id: int) -> List[dict]:
    """获取邀请人所有邀请奖励记录"""
    db = next(get_db())
    rewards = db.query(InviteReward).filter(
        InviteReward.inviter_id == inviter_id
    ).order_by(InviteReward.created_at.desc()).all()
    
    return [
        {
            "id": r.id,
            "invitee_id": r.invitee_id,
            "reward_credits": r.reward_credits,
            "status": r.status,
            "created_at": r.created_at.isoformat() if r.created_at else None
        }
        for r in rewards
    ]


# ========== 邀请奖励触发与防刷 ==========

INVITE_REWARD_EXPIRE_DAYS = 7  # 邀请奖励有效期（天）
MAX_DAILY_INVITE_REWARDS = 3   # 每人每日通过邀请获得的最大奖励次数


def get_pending_invite_reward_by_invitee(invitee_id: int) -> Optional[InviteReward]:
    """获取被邀请人待完成的邀请奖励记录"""
    db = next(get_db())
    return db.query(InviteReward).filter(
        InviteReward.invitee_id == invitee_id,
        InviteReward.status == "pending"
    ).first()


def get_today_invite_reward_count(inviter_id: int) -> int:
    """获取邀请人今日已通过邀请获得的奖励次数"""
    db = next(get_db())
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return db.query(InviteReward).filter(
        InviteReward.inviter_id == inviter_id,
        InviteReward.status == "completed",
        InviteReward.reward_granted_at >= today_start
    ).count()


def check_invite_reward_expired(reward: InviteReward) -> bool:
    """检查邀请奖励是否已过期（超过7天未完成首次审查）"""
    if not reward:
        return True
    expire_at = reward.created_at + timedelta(days=INVITE_REWARD_EXPIRE_DAYS)
    return datetime.now() > expire_at


def complete_invite_reward(invitee_id: int) -> dict:
    """
    被邀请人完成首次有效审查后触发奖励发放
    返回: {"success": bool, "message": str, "inviter_credits": int, "invitee_credits": int}
    """
    import logging
    logger = logging.getLogger(__name__)
    
    db = next(get_db())
    
    try:
        # 查找待完成的邀请记录
        reward = db.query(InviteReward).filter(
            InviteReward.invitee_id == invitee_id,
            InviteReward.status == "pending"
        ).first()
        
        if not reward:
            logger.info(f"[INVITE_REWARD] 用户 {invitee_id} 无待完成的邀请记录")
            return {"success": False, "message": "无待完成的邀请记录"}
        
        logger.info(f"[INVITE_REWARD] 找到待处理邀请记录 - 邀请人:{reward.inviter_id}, 被邀请人:{invitee_id}, 奖励额度:{reward.reward_credits}, 创建时间:{reward.created_at}")
        
        # 检查是否已过期
        if check_invite_reward_expired(reward):
            reward.status = "expired"
            db.commit()
            logger.warning(f"[INVITE_REWARD] 邀请奖励已过期 - 邀请人:{reward.inviter_id}, 被邀请人:{invitee_id}, 创建时间:{reward.created_at}")
            return {"success": False, "message": "邀请奖励已过期（超过7天未完成首次审查）"}
        
        # 检查邀请人今日奖励上限
        today_count = get_today_invite_reward_count(reward.inviter_id)
        logger.info(f"[INVITE_REWARD] 邀请人 {reward.inviter_id} 今日已完成奖励次数: {today_count}/{MAX_DAILY_INVITE_REWARDS}")
        if today_count >= MAX_DAILY_INVITE_REWARDS:
            logger.warning(f"[INVITE_REWARD] 邀请人 {reward.inviter_id} 今日奖励已达上限")
            return {"success": False, "message": "邀请人今日奖励已达上限"}
        
        # 给邀请人增加额度
        inviter_user = db.query(User).filter(User.id == reward.inviter_id).first()
        if inviter_user:
            inviter_before = inviter_user.bonus_credits
            inviter_user.bonus_credits += reward.reward_credits
            logger.info(f"[INVITE_REWARD] 邀请人 {reward.inviter_id} 额度变更: {inviter_before} -> {inviter_user.bonus_credits} (+{reward.reward_credits})")
        else:
            logger.error(f"[INVITE_REWARD] 邀请人 {reward.inviter_id} 不存在！")
            return {"success": False, "message": f"邀请人用户不存在(id={reward.inviter_id})"}
        
        # 给被邀请人增加额度
        invitee_user = db.query(User).filter(User.id == invitee_id).first()
        if invitee_user:
            invitee_before = invitee_user.bonus_credits
            invitee_user.bonus_credits += reward.reward_credits
            logger.info(f"[INVITE_REWARD] 被邀请人 {invitee_id} 额度变更: {invitee_before} -> {invitee_user.bonus_credits} (+{reward.reward_credits})")
        else:
            logger.error(f"[INVITE_REWARD] 被邀请人 {invitee_id} 不存在！")
            return {"success": False, "message": f"被邀请人用户不存在(id={invitee_id})"}
        
        # 更新邀请记录状态
        reward.status = "completed"
        reward.invitee_first_review_at = datetime.now()
        reward.reward_granted_at = datetime.now()
        
        db.commit()
        logger.info(f"[INVITE_REWARD] ✅ 邀请奖励发放成功 - 邀请人:{reward.inviter_id}(+{reward.reward_credits}), 被邀请人:{invitee_id}(+{reward.reward_credits})")
        
        return {
            "success": True,
            "message": "邀请奖励发放成功",
            "inviter_credits": reward.reward_credits,
            "invitee_credits": reward.reward_credits
        }
    except Exception as e:
        db.rollback()
        logger.error(f"[INVITE_REWARD] 邀请奖励发放异常: {e}", exc_info=True)
        return {"success": False, "message": f"邀请奖励发放失败: {str(e)}"}
    finally:
        db.close()


def expire_old_invite_rewards() -> int:
    """将超过7天未完成的邀请记录标记为过期，返回过期数量"""
    db = next(get_db())
    cutoff_date = datetime.now() - timedelta(days=INVITE_REWARD_EXPIRE_DAYS)
    
    expired_rewards = db.query(InviteReward).filter(
        InviteReward.status == "pending",
        InviteReward.created_at < cutoff_date
    ).all()
    
    count = 0
    for reward in expired_rewards:
        reward.status = "expired"
        count += 1
    
    db.commit()
    return count


# ========== 用户管理（管理员接口）==========

def get_users(
    page: int = 1,
    limit: int = 20,
    mobile: str = None,
    status: str = None
) -> dict:
    """获取用户列表（分页），支持按手机号搜索和状态筛选"""
    db = next(get_db())
    query = db.query(User).order_by(User.created_at.desc())
    
    if mobile:
        query = query.filter(User.mobile.like(f'%{mobile}%'))
    
    if status:
        query = query.filter(User.status == status)
    
    total = query.count()
    offset = (page - 1) * limit
    users = query.offset(offset).limit(limit).all()
    
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "country_code": user.country_code,
            "mobile": user.mobile,
            "bonus_credits": user.bonus_credits,
            "status": user.status,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_active_at": user.last_active_at.isoformat() if user.last_active_at else None,
            "invited_by": user.invited_by
        })
    
    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }


def get_user_detail(user_id: int) -> dict:
    """获取用户详情"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return None
    
    return {
        "id": user.id,
        "country_code": user.country_code,
        "mobile": user.mobile,
        "bonus_credits": user.bonus_credits,
        "status": user.status,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_active_at": user.last_active_at.isoformat() if user.last_active_at else None,
        "invited_by": user.invited_by
    }


def update_user_status(user_id: int, status: str) -> bool:
    """更新用户状态"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return False
    
    user.status = status
    db.commit()
    return True


def approve_user(user_id: int) -> bool:
    """审核通过用户（pending -> normal）"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user or user.status != "pending":
        return False
    
    user.status = "normal"
    db.commit()
    return True


def create_user_by_admin(mobile: str, password_hash: str, country_code: str = "+86", bonus_credits: int = 3) -> User:
    """管理员手动创建用户，默认状态为normal（已审核）"""
    db = next(get_db())
    user = User(
        country_code=country_code,
        mobile=mobile,
        password_hash=password_hash,
        status="normal",
        bonus_credits=bonus_credits
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise ValueError("该手机号已存在")


def add_user_credits(user_id: int, amount: int) -> int:
    """增加用户额度，返回更新后的额度"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return 0
    
    user.bonus_credits += amount
    db.commit()
    db.refresh(user)
    return user.bonus_credits


def reduce_user_credits(user_id: int, amount: int) -> int:
    """减少用户额度，返回更新后的额度"""
    db = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return 0
    
    user.bonus_credits = max(0, user.bonus_credits - amount)
    db.commit()
    db.refresh(user)
    return user.bonus_credits


def get_user_records(user_id: int, page: int = 1, limit: int = 20) -> dict:
    """获取用户审查记录（分页）"""
    db = next(get_db())
    from sqlalchemy import desc
    
    query = db.query(Record).filter(Record.user_id == user_id).order_by(desc(Record.created_at))
    total = query.count()
    offset = (page - 1) * limit
    records = query.offset(offset).limit(limit).all()
    
    result = []
    for record in records:
        metadata = json.loads(record.metadata_json) if record.metadata_json else {}
        result.append({
            "id": record.id,
            "filename": record.filename,
            "report_markdown": record.report_markdown,
            "raw_output": record.raw_output,
            "metadata": metadata,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        })
    
    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }


def get_admin_logs_by_target(target_type: str, target_value: str, page: int = 1, limit: int = 20) -> dict:
    """获取针对特定目标的管理员操作日志"""
    db = next(get_db())
    from sqlalchemy import desc
    
    query = db.query(AdminLog).filter(
        AdminLog.target_type == target_type,
        AdminLog.target_value == target_value
    ).order_by(desc(AdminLog.created_at))
    
    total = query.count()
    offset = (page - 1) * limit
    logs = query.offset(offset).limit(limit).all()
    
    result = []
    for log in logs:
        result.append({
            "id": log.id,
            "admin_user": log.admin_user,
            "action": log.action,
            "target_type": log.target_type,
            "target_value": log.target_value,
            "detail": log.detail,
            "created_at": log.created_at.isoformat() if log.created_at else None
        })
    
    return {
        "data": result,
        "total": total,
        "page": page,
        "limit": limit
    }


def create_admin_log(admin_user: str, action: str, target_type: str, target_value: str, detail: str = None) -> None:
    """创建管理员操作日志"""
    db = next(get_db())
    log = AdminLog(
        admin_user=admin_user,
        action=action,
        target_type=target_type,
        target_value=str(target_value),
        detail=detail
    )
    db.add(log)
    db.commit()


# ========== 文件哈希缓存管理（重复上传检测）==========

def calculate_file_hash(content: bytes) -> str:
    """计算文件内容的MD5哈希值"""
    return hashlib.md5(content).hexdigest()


def get_file_hash_cache(user_id: int, file_hash: str) -> Optional[FileHashCache]:
    """检查用户是否上传过相同文件"""
    db = next(get_db())
    return db.query(FileHashCache).filter(
        FileHashCache.user_id == user_id,
        FileHashCache.file_hash == file_hash
    ).first()


def create_or_update_file_hash_cache(user_id: int, file_hash: str, filename: str) -> None:
    """创建或更新文件哈希缓存记录"""
    db = next(get_db())
    
    existing = db.query(FileHashCache).filter(
        FileHashCache.user_id == user_id,
        FileHashCache.file_hash == file_hash
    ).first()
    
    if existing:
        # 更新现有记录
        existing.last_upload_time = datetime.now()
        existing.upload_count += 1
        if filename:
            existing.filename = filename
    else:
        # 创建新记录
        cache = FileHashCache(
            user_id=user_id,
            file_hash=file_hash,
            filename=filename
        )
        db.add(cache)
    
    db.commit()
