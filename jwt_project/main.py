# This is the code for the JWT authentication system with FastAPI.

from fastapi import APIRouter, Depends, HTTPException, status, Security,FastAPI
from pydantic import BaseModel, Field
import jwt
from jose import JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import create_engine, String, Integer, Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional
import uvicorn
# FastAPI 应用
app = FastAPI()

class Base(DeclarativeBase):
    pass

# 设置和依赖
SECRET_KEY = "jowewclaksidfoiawerlkasdf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 创建数据库引擎
DATABASE_URL = "mysql://root:ygnmygh@localhost/jwt_db"
engine = create_engine(DATABASE_URL, echo=True)  # echo=True 用于打印SQL日志，可根据需要开启或关闭
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建会话局部会话

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class LoginHistory(Base):
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_agent = Column(String)
    datetime = Column(String)
    user = relationship("User", back_populates="login_history")

User.login_history = relationship("LoginHistory", order_by=LoginHistory.id, back_populates="user")


# JWT 令牌模型
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user(db: Session = Depends(get_db), token: str = Security(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# 登录和注册端点
@app.post("/register", response_model=Token)
async def register(email: str, password: str, db: SessionLocal = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    access_token_expires = timedelta(minutes=30)  # 例如，30分钟过期
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=30)  # 例如，30分钟过期
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# 刷新令牌端点
@app.post("/refresh", response_model=Token)
async def refresh(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = get_current_user(db, token)  # 正确传递 token 和 db
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": current_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# 用户信息更新端点
@app.put("/user/update", response_model=Token)
async def update_user(email: str, password: str,
                      current_user: User = Depends(get_current_active_user),
                      db: SessionLocal = Depends(get_db)):
    if email != current_user.email:
        current_user.email = email
    hashed_password = get_password_hash(password)
    current_user.hashed_password = hashed_password
    db.commit()
    access_token_expires = timedelta(minutes=30)  # 例如，30分钟过期
    access_token = create_access_token(data={"sub": current_user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# 用户登录历史端点
@app.get("/user/history", response_model=list)
async def user_history(current_user: User = Depends(get_current_active_user), db: SessionLocal = Depends(get_db)):
    return db.query(LoginHistory).filter(LoginHistory.user_id == current_user.id).all()

# 注销端点
@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    # 这里应该实现令牌失效的逻辑，可能涉及到将令牌添加到黑名单中
    # 由于这个示例中没有实现 Redis，所以这个端点暂时不会做任何操作
    return {"msg": "Logged out"}

# JWT 令牌创建函数
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # 确保 expires_delta 是 timedelta 对象
    to_encode.update({"exp": expire})
    try:
        # 使用 PyJWT 的 encode 方法
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt  # 直接返回 encoded_jwt，因为它已经是字符串类型
    except PyJWTError as e:
        # 处理可能的 JWT 编码错误
        return str(e)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)