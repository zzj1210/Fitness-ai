# E:\Fitness-ai-backend\app\models\user.py
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime,timezone
from app.database import Base

class User(Base):
    """用户数据模型"""
    __tablename__ = "users"  # 数据库表名
    records = relationship("ExerciseRecord", back_populates="user", cascade="all, delete-orphan")

    id = Column(Integer, primary_key=True, index=True)  # 主键
    username = Column(String(50), unique=True, index=True, nullable=False)  # 用户名
    email = Column(String(100), unique=True, index=True, nullable=False)  # 邮箱
    password_hash = Column(String(255), nullable=False)  # 加密后的密码
    is_active = Column(Boolean, default=True)  # 账户是否激活
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # 修改
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))  # 修改
    
    def __repr__(self):
        return f"<User {self.username}>"