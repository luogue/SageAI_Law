"""数据库迁移脚本模板 - 初始版本"""
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """执行迁移"""
    # 创建所有表（首次部署时使用）
    # 如果已有 migrate_db.py，则复用其逻辑
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from storage.database import init_db
    init_db()


def downgrade():
    """回滚迁移（SQLite 不支持 DROP COLUMN，仅删表重建）"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from storage.database import Base, engine
    Base.metadata.drop_all(engine)
