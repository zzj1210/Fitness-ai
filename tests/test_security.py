from app.utils.security import hash_password, verify_password, create_access_token


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
        # 但都能验证通过
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
