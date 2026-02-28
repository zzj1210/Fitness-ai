# E:\Fitness-ai-backend\scripts\init_db.py

from app.database import engine, Base
from app.models import *  # 自动导入所有模型


def init_database():
    """初始化数据库表"""
    # 根据模型创建表
    Base.metadata.create_all(bind=engine)
    print("[OK] 数据库表创建成功！")
    print("[OK] 已创建表：users, exercises, records")


if __name__ == "__main__":
    init_database()
