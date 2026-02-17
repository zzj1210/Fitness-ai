# E:\Fitness-ai-backend\app\main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, exercise

app = FastAPI(
    title="体适能AI管家 API",
    description="校园健康体适能检测与管理系统",
    version="1.0.0"
)

# 允许跨域（开发环境）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(exercise.router, prefix="/api/exercise", tags=["运动"])

@app.get("/")
def root():
    return {"message": "欢迎使用体适能AI管家 API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}