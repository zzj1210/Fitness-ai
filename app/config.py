# E:\Fitness-ai-backend\app\config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 数据库
    DATABASE_URL: str = "postgresql://acidmoon:132456758@localhost:5432/fitness_ai"
    
    class Config:
        env_file = ".env"

settings = Settings()