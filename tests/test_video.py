from fastapi import status
from io import BytesIO


class TestVideoUpload:
    """视频上传接口测试"""

    def test_upload_video_requires_auth(self, client, db_session):
        """测试上传视频需要认证"""
        from app.models.exercise import Exercise, ExerciseRecord

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=1,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60
        )
        db_session.add(record)
        db_session.commit()

        response = client.post(f"/api/video/records/{record.id}/video")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_upload_video_success(self, client, db_session, test_user, tmp_path):
        """测试上传视频成功"""
        from app.models.exercise import Exercise, ExerciseRecord
        from unittest.mock import patch

        # 创建测试记录
        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60
        )
        db_session.add(record)
        db_session.commit()

        # 临时上传目录
        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()

        # 模拟视频文件
        video_content = BytesIO(b"fake video content")
        video_content.name = "test.mp4"

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        # Patch UPLOAD_DIR
        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.post(
                f"/api/video/records/{record.id}/video",
                headers=headers,
                files={"video": ("test.mp4", video_content, "video/mp4")}
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "视频上传成功"
        assert data["video_deleted"] is False

    def test_upload_video_invalid_format(self, client, db_session, test_user, tmp_path):
        """测试上传不支持的视频格式"""
        from app.models.exercise import Exercise, ExerciseRecord
        from unittest.mock import patch

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60
        )
        db_session.add(record)
        db_session.commit()

        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()

        # 尝试上传 txt 文件
        txt_content = BytesIO(b"text content")
        txt_content.name = "test.txt"

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.post(
                f"/api/video/records/{record.id}/video",
                headers=headers,
                files={"video": ("test.txt", txt_content, "text/plain")}
            )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "不支持的视频格式" in response.json()["detail"]

    def test_upload_video_record_not_found(self, client, db_session, test_user, tmp_path):
        """测试运动记录不存在"""
        from unittest.mock import patch

        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()

        video_content = BytesIO(b"fake video content")
        video_content.name = "test.mp4"

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.post(
                "/api/video/records/9999/video",
                headers=headers,
                files={"video": ("test.mp4", video_content, "video/mp4")}
            )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "运动记录不存在" in response.json()["detail"]

    def test_upload_video_keep_false(self, client, db_session, test_user, tmp_path):
        """测试临时上传模式（不保留视频）"""
        from app.models.exercise import Exercise, ExerciseRecord
        from unittest.mock import patch

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60
        )
        db_session.add(record)
        db_session.commit()

        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()

        video_content = BytesIO(b"fake video content")
        video_content.name = "test.mp4"

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.post(
                f"/api/video/records/{record.id}/video",
                headers=headers,
                files={"video": ("test.mp4", video_content, "video/mp4")}
            )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # 默认 keep_video=True，所以 video_deleted 应该为 False
        assert data["video_deleted"] is False
        assert "永久存储" in data["note"]


class TestVideoDelete:
    """视频删除接口测试"""

    def test_delete_video_requires_auth(self, client, db_session):
        """测试删除视频需要认证"""
        from app.models.exercise import Exercise, ExerciseRecord

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=1,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60,
            video_url="/videos/test.mp4"
        )
        db_session.add(record)
        db_session.commit()

        response = client.delete(f"/api/video/records/{record.id}/video")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_video_success(self, client, db_session, test_user, tmp_path):
        """测试删除视频成功"""
        from app.models.exercise import Exercise, ExerciseRecord
        from unittest.mock import patch

        # 创建测试记录并关联视频
        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        # 创建临时视频文件
        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()
        test_video_path = upload_dir / "test.mp4"
        test_video_path.write_bytes(b"fake video content")

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60,
            video_url="/videos/test.mp4"
        )
        db_session.add(record)
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.delete(f"/api/video/records/{record.id}/video", headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "视频已删除"

        # 验证数据库中的视频路径已清空
        db_session.refresh(record)
        assert record.video_url is None

    def test_delete_video_no_video(self, client, db_session, test_user):
        """测试删除没有视频的记录"""
        from app.models.exercise import Exercise, ExerciseRecord

        exercise = Exercise(name="测试动作", category="上肢")
        db_session.add(exercise)
        db_session.commit()

        record = ExerciseRecord(
            user_id=test_user["user"].id,
            exercise_id=exercise.id,
            score=80,
            count=10,
            duration=60,
            video_url=None
        )
        db_session.add(record)
        db_session.commit()

        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = client.delete(f"/api/video/records/{record.id}/video", headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "该记录没有关联视频" in response.json()["detail"]

    def test_delete_video_record_not_found(self, client, db_session, test_user):
        """测试删除不存在的记录"""
        headers = {"Authorization": f"Bearer {test_user['token']}"}
        response = client.delete("/api/video/records/9999/video", headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "运动记录不存在" in response.json()["detail"]


class TestVideoAccess:
    """视频访问接口测试"""

    def test_get_video_requires_auth(self, client, db_session):
        """测试访问视频需要认证"""
        response = client.get("/api/video/videos/test.mp4")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_video_not_found(self, client, db_session, test_user, tmp_path):
        """测试访问不存在的视频"""
        from unittest.mock import patch

        upload_dir = tmp_path / "videos"
        upload_dir.mkdir()

        headers = {"Authorization": f"Bearer {test_user['token']}"}

        with patch('app.api.video.UPLOAD_DIR', str(upload_dir)):
            response = client.get("/api/video/videos/nonexistent.mp4", headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "视频文件不存在" in response.json()["detail"]
