# E:\Fitness-ai-backend\app\schemas\stats.py

from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

# 运动统计响应
class ExerciseStats(BaseModel):
    total_sessions: int  # 总运动次数
    total_repetitions: int  # 总完成次数
    average_score: float  # 平均得分
    best_score: float  # 最高得分
    total_duration: int  # 总时长 (秒)
    
    class Config:
        from_attributes = True

# 按动作分类统计
class CategoryStats(BaseModel):
    category: str
    count: int
    average_score: float

# 最近运动记录（用于趋势图）
class RecentRecord(BaseModel):
    id: int
    exercise_name: str
    score: float
    count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 综合统计响应
class StatsSummary(BaseModel):
    exercise_stats: ExerciseStats
    category_stats: List[CategoryStats]
    recent_records: List[RecentRecord]