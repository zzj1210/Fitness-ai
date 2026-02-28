# E:\Fitness-ai-backend\app\exceptions.py

from fastapi import Request
from fastapi.responses import JSONResponse
from loguru import logger


class BusinessException(Exception):
    """业务异常 - 用户可理解的错误"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class SystemException(Exception):
    """系统异常 - 需要告警的错误"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


async def business_exception_handler(request: Request, exc: BusinessException):
    """业务异常处理器"""
    logger.warning(
        f"Business error: {exc.message} - Path: {request.url.path}",
        extra={"event": "error.business", "path": str(request.url.path)},
    )

    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


async def system_exception_handler(request: Request, exc: SystemException):
    """系统异常处理器"""
    logger.error(
        f"System error: {exc.message} - Path: {request.url.path}",
        extra={"event": "error.system", "path": str(request.url.path)},
        exc_info=True,
    )

    return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})


async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器（捕获所有未处理的异常）"""
    logger.error(
        f"Unhandled error: {str(exc)} - Path: {request.url.path}",
        extra={"event": "error.unhandled", "path": str(request.url.path)},
        exc_info=True,
    )

    return JSONResponse(status_code=500, content={"detail": "服务器内部错误"})


# 注册异常处理器
def register_exception_handlers(app):
    """注册所有异常处理器到 FastAPI 应用"""
    app.add_exception_handler(BusinessException, business_exception_handler)
    app.add_exception_handler(SystemException, system_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)


__all__ = ["BusinessException", "SystemException", "register_exception_handlers"]
