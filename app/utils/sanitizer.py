# E:\Fitness-ai-backend\app\utils\sanitizer.py


def sanitize_password(password: str) -> str:
    """密码脱敏"""
    return "***"


def sanitize_email(email: str) -> str:
    """邮箱脱敏"""
    if "@" not in email:
        return email
    username, domain = email.split("@")
    if len(username) == 0:
        return f"***@{domain}"
    return f"{username[0]}***@{domain}"


def sanitize_token(token: str) -> str:
    """Token 脱敏"""
    if len(token) <= 6:
        return "***"
    return f"{token[:3]}***{token[-3:]}"


def sanitize_ip(ip: str) -> str:
    """IP 地址脱敏"""
    parts = ip.split(".")
    if len(parts) == 4:
        return ".".join(parts[:3] + ["***"])
    return ip


def sanitize_username(username: str) -> str:
    """用户名脱敏"""
    if len(username) <= 2:
        return username[0] + "***"
    return f"{username[0]}{username[1]}***"
