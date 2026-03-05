# E:\Fitness-ai-backend\app\api\exercise.py

from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.exercise import Exercise, ExerciseRecord
from app.schemas.exercise import (
    ExerciseRecordCreate,
    ExerciseRecordResponse,
    ExerciseResponse,
    ExerciseRecordUpdate,
)
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/records", response_model=ExerciseRecordResponse)
def create_record(
    record_data: ExerciseRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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
        feedback=record_data.feedback,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/records", response_model=List[ExerciseRecordResponse])
def get_user_records(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    exercise_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用户运动记录（支持日期范围、动作 ID 过滤）"""
    query = db.query(ExerciseRecord).filter(ExerciseRecord.user_id == current_user.id)

    if start_date:
        query = query.filter(
            ExerciseRecord.created_at
            >= datetime.combine(start_date, datetime.min.time())
        )
    if end_date:
        query = query.filter(
            ExerciseRecord.created_at <= datetime.combine(end_date, datetime.max.time())
        )
    if exercise_id:
        query = query.filter(ExerciseRecord.exercise_id == exercise_id)

    records = (
        query.order_by(ExerciseRecord.created_at.desc()).offset(skip).limit(limit).all()
    )
    return records


@router.get("/exercises", response_model=List[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    """获取标准动作列表"""
    exercises = db.query(Exercise).all()
    return exercises


@router.put("/records/{record_id}", response_model=ExerciseRecordResponse)
def update_record(
    record_id: int,
    record_data: ExerciseRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改运动记录"""
    db_record = (
        db.query(ExerciseRecord)
        .filter(
            ExerciseRecord.id == record_id, ExerciseRecord.user_id == current_user.id
        )
        .first()
    )
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")

    # 只更新提供的字段
    update_data = record_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_record, field, value)

    db.commit()
    db.refresh(db_record)
    return db_record


@router.delete("/records/{record_id}")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除运动记录"""
    db_record = (
        db.query(ExerciseRecord)
        .filter(
            ExerciseRecord.id == record_id, ExerciseRecord.user_id == current_user.id
        )
        .first()
    )
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")

    db.delete(db_record)
    db.commit()
    return {"message": "删除成功"}


@router.delete("/records")
def batch_delete_records(
    record_ids: List[int] = Query(..., description="要删除的记录 ID 列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """批量删除运动记录"""
    db.query(ExerciseRecord).filter(
        ExerciseRecord.id.in_(record_ids),
        ExerciseRecord.user_id == current_user.id,
    ).delete(synchronize_session=False)

    db.commit()
    return {"message": f"成功删除 {len(record_ids)} 条记录"}
