# E:\Fitness-ai-backend\app\config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # 数据库
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/fitness_ai"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS 配置
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "7 days"
    LOG_FORMAT: str = "text"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def allowed_origins_list(self) -> List[str]:
        """将逗号分隔的字符串转换为列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
