### 后端技术栈
| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.129.0 |
| 服务器 | Uvicorn | 0.41.0 |
| 数据库 | PostgreSQL | 14+ |
| 密码加密 | bcrypt | 5.0.0 |
| JWT 令牌 | python-jose | 3.5.0 |
| 数据验证 | Pydantic | 2.12.5 |
| Python 版本 | Python | 3.13.9 |

### 项目结构（截至2.24）
```
.\Fitness-ai-backend\ 
├── app/
│   ├── main.py              # FastAPI 主入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接配置
│   ├── api/
│   │   ├── auth.py          # 认证接口（注册/登录）
│   │   ├── exercise.py      # 运动接口（动作库/记录）
│   │   ├── stats.py         # 数据统计接口
│   │   ├── video.py         # 视频上传与删除接口(可选保存或不上传服务器)
│   ├── models/
│   │   ├── _init_.py
│   │   ├── user.py          # 用户数据模型
│   │   └── exercise.py      # 运动数据模型
│   ├── schemas/
│   │   ├── _init_.py
│   │   ├── user.py          # 用户数据验证
│   │   ├── exercise.py      # 运动数据验证
│   │   ├── stats.py         # 数据统计模型
│   └── utils/
│       └── security.py      # 密码加密/JWT/认证
├── uploads
│   └── videos/              # 上传视频存储  
├── tests/
│   ├── conftest.py             # 测试配置
│   ├── test_auth.py            # 认证测试
│   ├── test_exercise.py        # 运动记录测试
│   ├── test_stats.py           # 统计测试
│   └── test_security.py        # 安全工具测试 
├── _init_db.py              # 数据库初始化脚本
├── seed_data.py             # 测试数据种子脚本
├── .env.example             # 环境变量模板
├── requirements.txt         # 依赖列表
├── td.py                    # 数据库连接测试
├── pytest.ini                  # pytest 配置
└── .gitignore
```

### 从源码构建（开发者）
```
# 1. 克隆仓库
git clone https://github.com/Acidmoon/Fitness-ai.git
cd Fitness-ai

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境 (Windows PowerShell)
venv\Scripts\Activate.ps1

# 4. 安装依赖
pip install -r requirements.txt


# 5. 配置环境变量
copy .env.example .env
# 生成安全密钥
python -c "import secrets; print(secrets.token_hex(32))"

# 编辑 .env 文件，填入实际配置

# 6. 初始化数据库
python _init_db.py
python seed_data.py

# 7. 启动服务
uvicorn app.main:app --reload

# 启动成功后服务端口在http://127.0.0.1:8000
# API 文档地址
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
# Ctrl C 结束服务


```
