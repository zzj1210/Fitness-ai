# Fitness-ai Backend

校园健康体适能检测与管理系统的后端服务，基于 FastAPI 构建，提供用户认证、运动记录管理、数据统计和视频上传等功能。

---

## 📋 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [API 接口概览](#api-接口概览)
- [快速开始](#快速开始)
- [运行测试](#运行测试)
- [开发进度](#开发进度)

---

## 🛠 技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| Web 框架 | FastAPI | 0.129.0 | 高性能异步 API 框架 |
| ASGI 服务器 | Uvicorn | 0.41.0 | Python ASGI 服务器 |
| 数据库 | PostgreSQL | 14+ | 关系型数据库 |
| ORM | SQLAlchemy | 2.0.46 | Python SQL 工具包 |
| 密码加密 | bcrypt | 5.0.0 | 密码哈希库 |
| JWT 令牌 | python-jose | 3.5.0 | JWT 生成与验证 |
| 数据验证 | Pydantic | 2.12.5 | 数据验证与解析 |
| Python | Python | 3.13.9 | 运行环境 |

---

## 📁 项目结构

```
Fitness-ai-backend/
├── app/
│   ├── main.py                 # FastAPI 应用入口
│   ├── config.py               # 配置文件 (环境变量)
│   ├── database.py             # 数据库连接
│   ├── logging_config.py       # 日志系统配置
│   ├── exceptions.py           # 异常处理
│   ├── api/
│   │   ├── auth.py             # 认证接口 (注册/登录)
│   │   ├── exercise.py         # 运动接口 (动作库/记录)
│   │   ├── stats.py            # 数据统计接口
│   │   ├── user.py             # 用户资料管理 (新增)
│   │   └── video.py            # 视频上传接口
│   ├── middleware/
│   │   ├── __init__.py         # 中间件模块
│   │   └── logging_middleware.py # 请求日志中间件
│   ├── models/
│   │   ├── __init__.py         # 模型导出
│   │   ├── user.py             # 用户数据模型
│   │   └── exercise.py         # 运动数据模型
│   ├── schemas/
│   │   ├── __init__.py         # Schema 导出
│   │   ├── user.py             # 用户数据验证
│   │   ├── exercise.py         # 运动数据验证
│   │   └── stats.py            # 数据统计模型
│   └── utils/
│       ├── sanitizer.py        # 敏感信息脱敏
│       └── security.py         # 密码加密/JWT/认证
├── tests/
│   ├── conftest.py             # 测试配置
│   ├── test_auth.py            # 认证模块测试
│   ├── test_exercise.py        # 运动记录测试
│   ├── test_stats.py           # 统计功能测试
│   ├── test_user.py            # 用户模块测试
│   └── test_video.py           # 视频模块测试
├── scripts/
│   ├── init_db.py              # 数据库初始化脚本
│   ├── seed_data.py            # 测试数据种子脚本
│   └── test_db.py              # 数据库连接测试
├── logs/                       # 日志目录 
│   └── app.log                 # 应用日志文件
├── uploads/videos/             # 视频存储目录
├── .env.example                # 环境变量模板
├── .flake8                     # flake8 配置
├── .gitignore                  # Git 忽略规则
├── pytest.ini                  # pytest 配置
├── requirements.txt            # 依赖列表
└── README.md                   # 项目文档
```

---

## 🔌 API 接口概览

### 认证模块 `/api/auth`
| 方法 | 路由 | 说明 | 认证 |
|------|------|------|------|
| POST | `/register` | 用户注册 | ❌ |
| POST | `/login` | 用户登录 | ❌ |

### 运动模块 `/api/exercise`
| 方法 | 路由 | 说明 | 认证 |
|------|------|------|------|
| POST | `/records` | 创建运动记录 | ✅ |
| GET | `/records` | 获取用户记录 (支持分页、日期范围、动作 ID 过滤) | ✅ |
| GET | `/exercises` | 获取标准动作列表 | ❌ |

### 统计模块 `/api/stats`
| 方法 | 路由 | 说明 | 认证 |
|------|------|------|------|
| GET | `/stats/summary` | 综合统计 | ✅ |
| GET | `/stats/weekly` | 周统计 | ✅ |
| GET | `/stats/personal-best` | 个人最佳 | ✅ |

### 视频模块 `/api/video`
| 方法 | 路由 | 说明 | 认证 |
|------|------|------|------|
| POST | `/records/{record_id}/video` | 上传视频 | ✅ |
| DELETE | `/records/{record_id}/video` | 删除视频 | ✅ |
| GET | `/videos/{filename}` | 访问视频 | ❌ |

### 用户模块 `/api/user`
| 方法 | 路由 | 说明 | 认证 |
|------|------|------|------|
| GET | `/profile` | 获取个人资料 | ✅ |
| PUT | `/profile` | 更新个人资料 | ✅ |
| PUT | `/password` | 修改密码 | ✅ |
| DELETE | `/account` | 注销账户（硬删除） | ✅ |

---

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/Acidmoon/Fitness-ai.git
cd Fitness-ai
```

### 2. 创建虚拟环境
```bash
python -m venv venv
```

### 3. 激活虚拟环境
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 4. 安装依赖
```bash
pip install -r requirements.txt
```

### 5. 配置环境变量
```bash
# 复制环境变量模板
copy .env.example .env

# 生成安全密钥
python -c "import secrets; print(secrets.token_hex(32))"
```

编辑 `.env` 文件，填入配置：
```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/fitness_ai
SECRET_KEY=your-random-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 6. 初始化数据库
```bash
python -m scripts.init_db
python -m scripts.seed_data
```

### 7. 启动服务
```bash
uvicorn app.main:app --reload
```

服务启动成功后访问：
- **服务地址**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json

---

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定模块
pytest -m tests.test_auth

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

当前测试状态：**52 个测试用例全部通过** 
测试覆盖率：**90%**

---

## 🛠 代码质量工具

### 格式化代码
```bash
black app/ tests/
```

### 检查代码风格
```bash
flake8 app/ tests/
```

当前代码状态：**flake8 检查通过** 

---

## 📝 日志系统

### 日志配置
日志系统使用 `loguru` 库，支持自动轮转和敏感信息脱敏。

**日志文件位置**: `logs/app.log`

**日志轮转策略**:
- 单个文件最大：10MB
- 保留时间：7 天
- 自动压缩备份文件

**敏感信息脱敏**:
- 密码：`***`
- 邮箱：`t***@example.com`
- Token: `eyJ***...`
- IP 地址：`192.168.1.***`

**查看日志**:
```bash
# 实时查看日志
tail -f logs/app.log

# 查看最近的日志
cat logs/app.log | tail -n 100
```

**日志级别配置** (`.env` 文件):
```bash
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT=text  # 或 json（生产环境）
```

---

## 📌 开发进度

### 已完成功能
- [x] 用户认证（注册/登录）
- [x] 用户资料管理（获取/更新/修改密码/注销）⭐ 新增
- [x] 运动记录管理（创建/查询）
- [x] 标准动作库
- [x] 数据统计接口
- [x] 视频上传功能
- [x] 日期范围过滤
- [x] 动作 ID 过滤
- [x] 测试体系建设（52 个测试用例）
- [x] 代码质量工具集成（black, flake8）
- [x] 视频模块测试（11 个测试用例，覆盖率 95%）
- [x] 日志系统 ⭐ 新增（敏感信息脱敏、请求日志、异常处理）

---

## 📎 附录

### 关键命令
```bash
# 生成安全密钥
python -c "import secrets; print(secrets.token_hex(32))"

# 数据库连接测试
python -m scripts.test_db

# 初始化数据库
python -m scripts.init_db

# 添加测试数据
python -m scripts.seed_data
```

---

**文档维护**: 请在每次重大更新后同步更新此文档
