import uvicorn
from fastapi import FastAPI, Path, Query, Body, Cookie, Header, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select, asc, delete, update
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapped, mapped_column
from typing import List, Dict
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Base(DeclarativeBase):
    pass


# Read environment variables
DB_DRIVER = "mysql+mysqldb"
DB_HOST = "localhost"
DB_PORT = "3306"
DB_USER = "root"
DB_PASSWORD = "ygnmygh"
DB_NAME = "testdb"

# Create database engine using environment variables
engine = create_engine(f'{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)



engine = create_engine('mysql+mysqldb://root:ygnmygh@localhost/testdb', echo=True)

# Define database models
class StudentEntity(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

class GroupEntity(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

class StudentGroupEntity(Base):
    __tablename__ = "student_group"
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, primary_key=True)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
app = FastAPI()

# Define API models
class StudentBase(BaseModel):
    id: int = Field(None, alias="id")
    name: str = Field(..., max_length=128)
    email: str = Field(..., max_length=128)

class StudentCreate(StudentBase):
    pass

class StudentUpdate(StudentBase):
    pass

class GroupBase(BaseModel):
    id: int = Field(None, alias="id")
    name: str = Field(..., max_length=128)

class GroupCreate(GroupBase):
    pass

class GroupUpdate(GroupBase):
    pass

def set_attrs(obj, data: dict):
    if data:
        for key, value in data.items():
            setattr(obj, key, value)

def get_db_session():
    db_session = Session()
    try:
        yield db_session
    finally:
        db_session.close()

def check_student_exist(student_id: int, db_session: Session):
    query = select(StudentEntity).where(StudentEntity.id == student_id)
    exist_student = db_session.execute(query).scalar()
    if not exist_student:
        raise HTTPException(status_code=404, detail=f'Student id({student_id}) not found')
    return exist_student

def check_group_exist(group_id: int, db_session: Session):
    query = select(GroupEntity).where(GroupEntity.id == group_id)
    exist_group = db_session.execute(query).scalar()
    if not exist_group:
        raise HTTPException(status_code=404, detail=f'Group id({group_id}) not found')
    return exist_group

@app.get(path='/students', response_model=List[StudentBase])
async def get_students(db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).order_by(asc(StudentEntity.name))
    return db_session.execute(query).scalars().all()

@app.post(path='/students', response_model=StudentBase)
async def create_student(student: StudentCreate, db_session: Session = Depends(get_db_session)):
    query = select(StudentEntity).where(StudentEntity.name == student.name)
    records = db_session.execute(query).scalars().all()
    if records:
        raise HTTPException(status_code=400, detail=f'Student {student.name} already exists')
    student_entity = StudentEntity(id=student.id, name=student.name, email=student.email)
    db_session.add(student_entity)
    db_session.commit()
    return student_entity

@app.get(path='/students/{student_id}', response_model=StudentBase)
async def get_student(student_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)
    return exist_student

@app.delete(path='/students/{student_id}', response_model=StudentBase)
async def delete_student(student_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)
    db_session.delete(exist_student)
    db_session.commit()
    return exist_student

@app.get(path='/groups', response_model=List[GroupBase])
async def get_groups(db_session: Session = Depends(get_db_session)):
    query = select(GroupEntity).order_by(asc(GroupEntity.name))
    return db_session.execute(query).scalars().all()

@app.post(path='/groups', response_model=GroupBase)
async def create_group(group: GroupCreate, db_session: Session = Depends(get_db_session)):
    query = select(GroupEntity).where(GroupEntity.name == group.name)
    records = db_session.execute(query).scalars().all()
    if records:
        raise HTTPException(status_code=400, detail=f'Group {group.name} already exists')
    group_entity = GroupEntity(id=group.id, name=group.name)
    db_session.add(group_entity)
    db_session.commit()
    return group_entity

@app.get(path='/groups/{group_id}', response_model=GroupBase)
async def get_group(group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_group = check_group_exist(group_id, db_session)
    return exist_group

@app.delete(path='/groups/{group_id}', response_model=GroupBase)
async def delete_group(group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_group = check_group_exist(group_id, db_session)
    db_session.delete(exist_group)
    db_session.commit()
    return exist_group

@app.post(path='/students/{student_id}/groups/{group_id}', response_model=StudentBase)
async def add_student_to_group(student_id: int = Path(...), group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)
    exist_group = check_group_exist(group_id, db_session)
    student_group_entity = StudentGroupEntity(student_id=student_id, group_id=group_id)
    db_session.add(student_group_entity)
    db_session.commit()
    return exist_student

@app.delete(path='/students/{student_id}/groups/{group_id}', response_model=StudentBase)
async def remove_student_from_group(student_id: int = Path(...), group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)
    exist_group = check_group_exist(group_id, db_session)
    query = delete(StudentGroupEntity).where(StudentGroupEntity.student_id == student_id, StudentGroupEntity.group_id == group_id)
    db_session.execute(query)
    db_session.commit()
    return exist_student

# @app.get(path='/groups/{group_id}/students', response_model=List[StudentBase])
# async def get_students_in_group(group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
#     exist_group = check_group_exist(group_id, db_session)
#     query = select(StudentEntity).join(StudentGroupEntity).where(StudentGroupEntity.group_id == group_id)
#     return db_session.execute(query).scalars().all()
@app.get(path='/groups/{group_id}/students', response_model=List[StudentBase])
async def get_students_in_group(group_id: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_group = check_group_exist(group_id, db_session)
    # 明确指定连接查询的表和条件
    query = select(StudentEntity).select_from(StudentGroupEntity).join(StudentEntity, StudentEntity.id == StudentGroupEntity.student_id).where(StudentGroupEntity.group_id == group_id)
    return db_session.execute(query).scalars().all()
@app.put(path='/students/{student_id}/groups/{group_id_from}/{group_id_to}', response_model=StudentBase)
async def transfer_student_between_groups(student_id: int = Path(...), group_id_from: int = Path(...), group_id_to: int = Path(...), db_session: Session = Depends(get_db_session)):
    exist_student = check_student_exist(student_id, db_session)
    exist_group_from = check_group_exist(group_id_from, db_session)
    exist_group_to = check_group_exist(group_id_to, db_session)
    query = delete(StudentGroupEntity).where(StudentGroupEntity.student_id == student_id, StudentGroupEntity.group_id == group_id_from)
    db_session.execute(query)
    new_student_group_entity = StudentGroupEntity(student_id=student_id, group_id=group_id_to)
    db_session.add(new_student_group_entity)
    db_session.commit()
    return exist_student

if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)