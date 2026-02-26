# E:\Fitness-ai-backend\scripts\init_db.py

from app.database import engine, Base

# 关键：必须导入所有模型，SQLAlchemy 才能创建对应的表
from app.models.user import User  # noqa: F401
from app.models.exercise import Exercise, ExerciseRecord  # noqa: F401


def init_database():
    """初始化数据库表"""
    # 根据模型创建表
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")
    print("✅ 已创建表：users, exercises, records")


if __name__ == "__main__":
    init_database()
