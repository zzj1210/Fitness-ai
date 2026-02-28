# E:\Fitness-ai-backend\app\middleware\logging_middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from loguru import logger
from app.utils.sanitizer import sanitize_ip


class LoggingMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""

    async def dispatch(self, request: Request, call_next):
        # 记录请求开始时间
        start_time = time.time()

        # 获取客户端 IP（脱敏）
        client_ip = request.client.host if request.client else "unknown"
        sanitized_ip = sanitize_ip(client_ip)

        # 获取请求信息
        method = request.method
        path = request.url.path

        try:
            # 执行请求
            response = await call_next(request)

            # 计算耗时
            duration = time.time() - start_time

            # 记录日志
            log_level = "INFO" if response.status_code < 400 else "WARNING"
            log_msg = (
                f"{method} {path} - {response.status_code} - "
                f"{duration * 1000:.2f}ms - IP: {sanitized_ip}"
            )
            logger.log(log_level, log_msg)

            return response

        except Exception as e:
            # 记录异常
            duration = time.time() - start_time
            log_msg = (
                f"{method} {path} - ERROR - {duration * 1000:.2f}ms - "
                f"IP: {sanitized_ip} - {str(e)}"
            )
            logger.error(log_msg, exc_info=True)
            raise


__all__ = ["LoggingMiddleware"]
