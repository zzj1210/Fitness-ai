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

### 项目结构(截至2.23）
```
.\Fitness-ai-backend\ 
├── app/
│   ├── main.py              # FastAPI 主入口
│   ├── config.py            # 配置文件
│   ├── database.py          # 数据库连接配置
│   ├── api/
│   │   ├── auth.py          # 认证接口（注册/登录）
│   │   ├── exercise.py      # 运动接口（动作库/记录）
│   ├── models/
│   │   ├── _init_.py
│   │   ├── user.py          # 用户数据模型
│   │   └── exercise.py      # 运动数据模型
│   ├── schemas/
│   │   ├── _init_.py
│   │   ├── user.py          # 用户数据验证
│   │   ├── exercise.py      # 运动数据验证
│   └── utils/
│       └── security.py      # 密码加密/JWT/认证
├── _init_db.py               # 数据库初始化脚本
├── seed_data.py             # 测试数据种子脚本
├── requirements.txt         # 依赖列表
├── td.py                    # 数据库连接测试
└── .gitignore
```

### 启动服务
```
# 进入项目文件夹
venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
