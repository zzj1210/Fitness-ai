# E:\Fitness-ai-backend\scripts\seed_data.py

from app.database import SessionLocal
from app.models.exercise import Exercise


def seed_exercises():
    db = SessionLocal()
    try:
        # 检查是否已有数据
        if db.query(Exercise).count() > 0:
            print("⚠️  动作库已有数据，跳过")
            return

        # 添加标准动作
        exercises = [
            Exercise(
                name="标准俯卧撑", category="上肢", description="双臂支撑，身体保持直线"
            ),
            Exercise(
                name="标准深蹲",
                category="下肢",
                description="双脚与肩同宽，下蹲至大腿平行地面",
            ),
            Exercise(
                name="平板支撑",
                category="核心",
                description="双臂支撑，身体保持直线，坚持时间",
            ),
            Exercise(
                name="仰卧起坐",
                category="核心",
                description="仰卧，双手抱头，起身至肘部触膝",
            ),
            Exercise(
                name="立定跳远", category="下肢", description="双脚起跳，测量跳跃距离"
            ),
        ]

        db.add_all(exercises)
        db.commit()
        print(f"✅ 已添加 {len(exercises)} 个标准动作")
    finally:
        db.close()


if __name__ == "__main__":
    seed_exercises()
