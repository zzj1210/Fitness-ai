# E:\Fitness-ai-backend\app\schemas\user.py

from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
import re


# 用户注册请求
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("密码至少 8 个字符")
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("密码必须包含字母")
        if not re.search(r"\d", v):
            raise ValueError("密码必须包含数字")
        return v


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

    model_config = ConfigDict(from_attributes=True)


# Token 响应
class Token(BaseModel):
    access_token: str
    token_type: str
