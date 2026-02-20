### 后端技术栈
| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.100+ |
| 服务器 | Uvicorn | 0.23+ |
| 数据库 | PostgreSQL | 14+ |
| 密码加密 | bcrypt | 3.2.2 |
| JWT 令牌 | python-jose | 3.3+ |
| 数据验证 | Pydantic | 2.0+ |
| Python 版本 | Python | 3.13 |

### 项目结构(截至2.20）
```
E:\Fitness-ai-backend\ 
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 主入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接配置
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py          # 认证接口（注册/登录）
│   │   ├── exercise.py      # 运动接口（动作库/记录）
│   │   └── stats.py         # 统计接口（数据分析）
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # 用户数据模型
│   │   └── exercise.py      # 运动数据模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # 用户数据验证
│   │   ├── exercise.py      # 运动数据验证
│   │   └── stats.py         # 统计数据验证
│   └── utils/
│       ├── __init__.py
│       └── security.py      # 密码加密/JWT/认证
├── venv/                    # 虚拟环境（不上传 Git）
├── init_db.py               # 数据库初始化脚本
├── seed_data.py             # 测试数据种子脚本
├── test_db.py               # 数据库连接测试
├── requirements.txt         # 依赖列表
└── .gitignore
```
