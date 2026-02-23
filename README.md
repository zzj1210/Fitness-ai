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

### 项目结构（截至2.23）
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
├── _init_db.py              # 数据库初始化脚本
├── seed_data.py             # 测试数据种子脚本
├── requirements.txt         # 依赖列表
├── td.py                    # 数据库连接测试
└── .gitignore
```

### 从源码构建（开发者）
```

#克隆仓库
git clone https://github.com/Acidmoon/Fitness-ai.git
cd Fitness-ai

# 创建虚拟环境
python -m venv venv 

# 激活虚拟环境，三选一
venv\Scripts\Activate.ps1 # Powershell下激活虚拟环境
venv\Scripts\activate.bat # cmd下激活
source venv/bin/activate # mac/Linux下

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python _init_db.py

# 启动后端服务
uvicorn app.main:app --reload

# 启动成功后服务端口在http://127.0.0.1:8000
# http://127.0.0.1:8000/docs      Swagger UI，FastAPI的文档，可以测试接口
# Ctrl C 结束服务


```
