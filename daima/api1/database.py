import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# 加载环境变量
load_dotenv()

# 从环境变量中获取数据库配置
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# 打印调试信息
print(f"DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}")

# 构建数据库 URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 获取数据库会话的生成器
def get_db():
    db = SessionLocal()
    try:
        yield db  # 使用 yield 使其成为生成器
    finally:
        db.close()  # 确保会话在完成后关闭
