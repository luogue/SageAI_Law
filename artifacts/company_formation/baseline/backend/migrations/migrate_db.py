"""数据库迁移脚本 - 添加邀请有礼功能模块"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from storage.database import Base, engine
from storage.models import User, Record, Blacklist, Feedback, BonusLog, RewardLog, InviteReward


def migrate():
    """执行数据库迁移"""
    print("开始数据库迁移...")
    
    Base.metadata.create_all(bind=engine)
    
    print("数据库迁移完成！")
    print("- User表：用户信息（含bonus_credits、invited_by字段）")
    print("- Record表：审查记录（不保存原始合同文本）")
    print("- Blacklist表：黑名单管理")
    print("- Feedback表：用户反馈（含质量评分字段）")
    print("- BonusLog表：额度赠送记录（用于每日限额）")
    print("- RewardLog表：奖励发放记录（记录每次奖励发放详情）")
    print("- InviteReward表：邀请奖励发放记录")


if __name__ == "__main__":
    migrate()