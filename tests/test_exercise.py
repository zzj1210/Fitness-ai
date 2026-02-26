from fastapi import status


class TestExerciseRecords:
    """运动记录测试"""

    def test_create_record_requires_auth(self, client, db_session):
        """测试创建记录需要认证"""
        response = client.post(
            "/api/exercise/records",
            json={"exercise_id": 1, "score": 85.5, "count": 20, "duration": 120},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_record_success(self, client, db_session, test_user):
        """测试创建记录成功"""
        # 先创建标准动作
        from app.models.exercise import Exercise

        exercise = Exercise(name="标准俯卧撑", category="上肢", description="测试动作")
        db_session.add(exercise)
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = client.post(
            "/api/exercise/records",
            json={
                "exercise_id": exercise.id,
                "score": 85.5,
                "count": 20,
                "duration": 120,
            },
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["score"] == 85.5
        assert data["count"] == 20

    def test_create_record_exercise_not_found(self, client, db_session, test_user):
        """测试动作不存在"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = client.post(
            "/api/exercise/records",
            json={"exercise_id": 999, "score": 85.5, "count": 20, "duration": 120},
            headers=headers,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "动作不存在" in response.json()["detail"]

    def test_get_user_records_requires_auth(self, client, db_session):
        """测试获取记录需要认证"""
        response = client.get("/api/exercise/records")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_user_records(self, client, db_session, test_user):
        """测试获取用户记录"""
        from app.models.exercise import Exercise, ExerciseRecord

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=85.5,
            count=20,
            duration=120,
        )
        db_session.add(record)
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = client.get("/api/exercise/records", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_user_records_with_date_range(self, client, db_session, test_user):
        """测试日期范围过滤"""
        from datetime import datetime, timedelta
        from app.models.exercise import Exercise, ExerciseRecord

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        today = datetime.now().date()

        record1 = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60,
            created_at=datetime.now() - timedelta(days=2),
        )
        record2 = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=85,
            count=15,
            duration=90,
            created_at=datetime.now() - timedelta(days=1),
        )
        record3 = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=90,
            count=20,
            duration=120,
            created_at=datetime.now(),
        )
        db_session.add_all([record1, record2, record3])
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        # 只查询最近 1 天的记录
        response = client.get(
            f"/api/exercise/records?start_date={today - timedelta(days=1)}",
            headers=headers,
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2

    def test_get_user_records_with_exercise_id_filter(
        self, client, db_session, test_user
    ):
        """测试动作 ID 过滤"""
        from app.models.exercise import Exercise, ExerciseRecord

        # 创建两个不同的动作
        exercise1 = Exercise(name="俯卧撑", category="上肢")
        exercise2 = Exercise(name="深蹲", category="下肢")
        db_session.add_all([exercise1, exercise2])
        db_session.commit()

        # 创建不同动作的记录
        record1 = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise1.id,
            score=80,
            count=10,
            duration=60,
        )
        record2 = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise2.id,
            score=85,
            count=15,
            duration=90,
        )
        db_session.add_all([record1, record2])
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        # 只查询 exercise1 的记录
        response = client.get(
            f"/api/exercise/records?exercise_id={exercise1.id}", headers=headers
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["exercise_id"] == exercise1.id

    def test_get_exercises(self, client, db_session):
        """测试获取标准动作列表（不需要认证）"""
        # 先创建测试动作
        from app.models.exercise import Exercise

        exercise = Exercise(name="标准俯卧撑", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        response = client.get("/api/exercise/exercises")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
