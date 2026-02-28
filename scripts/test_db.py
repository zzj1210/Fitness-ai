# E:\Fitness-ai-backend\scripts\test_db.py

from app.database import engine


def test_connection():
    try:
        # 尝试连接
        connection = engine.connect()
        print("[OK] 数据库连接成功！")
        connection.close()
        return True
    except Exception as e:
        print(f"[ERROR] 数据库连接失败：{e}")
        return False


if __name__ == "__main__":
    test_connection()
