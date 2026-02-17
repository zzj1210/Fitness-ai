# E:\Fitness-ai-backend\app\schemas\user.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 用户注册请求
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# 用户登录请求
class UserLogin(BaseModel):
    username: str
    password: str

# 用户响应（不包含密码）
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Token 响应
class Token(BaseModel):
    access_token: str
    token_type: str