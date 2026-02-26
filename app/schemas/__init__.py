# E:\Fitness-ai-backend\app\schemas\__init__.py

from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.schemas.exercise import (
    ExerciseRecordCreate,
    ExerciseRecordResponse,
    ExerciseResponse,
)
from app.schemas.stats import ExerciseStats, CategoryStats, RecentRecord, StatsSummary

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "ExerciseRecordCreate",
    "ExerciseRecordResponse",
    "ExerciseResponse",
    "ExerciseStats",
    "CategoryStats",
    "RecentRecord",
    "StatsSummary",
]
