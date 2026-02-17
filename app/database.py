# E:\Fitness-ai-backend\app\database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库连接 URL
# 格式：postgresql://用户名:密码@主机:端口/数据库名
DATABASE_URL = "postgresql://acidmoon:132456758@localhost:5432/fitness_ai"

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类（用于定义数据模型）
Base = declarative_base()

# 获取数据库会话的依赖函数（供 API 接口使用）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()