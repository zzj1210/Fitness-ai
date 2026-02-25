# E:\Fitness-ai-backend\app\api\exercise.py

from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.exercise import Exercise, ExerciseRecord
from app.schemas.exercise import ExerciseRecordCreate, ExerciseRecordResponse, ExerciseResponse
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/records", response_model=ExerciseRecordResponse)
def create_record(
    record_data: ExerciseRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建运动记录"""
    exercise = db.query(Exercise).filter(Exercise.id == record_data.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="动作不存在")
    
    db_record = ExerciseRecord(
        user_id=current_user.id,
        exercise_id=record_data.exercise_id,
        score=record_data.score,
        count=record_data.count,
        duration=record_data.duration,
        heart_rate_avg=record_data.heart_rate_avg,
        heart_rate_max=record_data.heart_rate_max,
        keypoints_data=record_data.keypoints_data,
        feedback=record_data.feedback
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/records", response_model=List[ExerciseRecordResponse])
def get_user_records(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户运动记录（支持日期范围过滤）"""
    query = db.query(ExerciseRecord).filter(
        ExerciseRecord.user_id == current_user.id
    )
    
    if start_date:
        query = query.filter(ExerciseRecord.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(ExerciseRecord.created_at <= datetime.combine(end_date, datetime.max.time()))
    
    records = query.order_by(ExerciseRecord.created_at.desc()).offset(skip).limit(limit).all()
    return records

@router.get("/exercises", response_model=List[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    """获取标准动作列表"""
    exercises = db.query(Exercise).all()
    return exercises
