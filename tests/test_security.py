from app.utils.security import hash_password, verify_password, create_access_token
from jose import jwt
from app.config import settings


class TestPasswordHashing:
    """密码加密测试"""

    def test_hash_password_returns_different_string(self):
        """测试加密后密码不同"""
        password = "password123"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_password_correct(self):
        """测试验证正确密码"""
        password = "password123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_wrong(self):
        """测试验证错误密码"""
        password = "password123"
        hashed = hash_password(password)
        assert verify_password("wrongpassword", hashed) is False

    def test_hash_password_different_salts(self):
        """测试每次加密结果不同（salt 不同）"""
        password = "password123"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)
        assert hashed1 != hashed2
        assert verify_password(password, hashed1) is True
        assert verify_password(password, hashed2) is True


class TestCreateAccessToken:
    """JWT 令牌测试"""

    def test_create_access_token_returns_string(self):
        """测试创建令牌返回字符串"""
        token = create_access_token({"sub": "testuser"})
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_different_payloads(self):
        """测试不同 payload 生成不同令牌"""
        token1 = create_access_token({"sub": "user1"})
        token2 = create_access_token({"sub": "user2"})
        assert token1 != token2

    def test_create_access_token_with_user_id(self):
        """测试使用 user_id 创建令牌"""
        user_id = 123
        token = create_access_token({"sub": str(user_id)})
        assert isinstance(token, str)
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert payload["sub"] == str(user_id)

    def test_token_sub_is_string(self):
        """测试 token sub 是字符串类型"""
        token = create_access_token({"sub": str(42)})
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        assert isinstance(payload["sub"], str)
