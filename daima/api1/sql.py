import sys
sys.path.append('D:\PyCharm Community Edition 2023.3.4\daima\api1')

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Session,declarative_base

Base = declarative_base()

from pydantic1 import Student,Group




# 关联表
student_group_association = Table(
    "student_group_association",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("group_id", Integer, ForeignKey("groups.id")),
)

# 数据模型
class StudentModel(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    groups = relationship("GroupModel", secondary=student_group_association, back_populates="students")

class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    students = relationship("StudentModel", secondary=student_group_association, back_populates="groups")

# 数据传输对象 (DTO)
class Student:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

class Group:
    def __init__(self, name: str):
        self.name = name

# 学生仓库
class StudentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, student: Student):
        db_student = StudentModel(name=student.name, email=student.email)
        self.db_session.add(db_student)
        self.db_session.commit()
        return db_student

    def get_all(self):
        return self.db_session.query(StudentModel).all()

    def get_by_id(self, student_id: int):
        return self.db_session.query(StudentModel).filter(StudentModel.id == student_id).first()

    def update(self, student_id: int, student: Student):
        db_student = self.get_by_id(student_id)
        if db_student:
            db_student.name = student.name
            db_student.email = student.email
            self.db_session.commit()
        return db_student

    def delete(self, student_id: int):
        db_student = self.get_by_id(student_id)
        if db_student:
            self.db_session.delete(db_student)
            self.db_session.commit()
            return True
        return False

# 组仓库
class GroupRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, group: Group):
        db_group = GroupModel(name=group.name)
        self.db_session.add(db_group)
        self.db_session.commit()
        return db_group

    def get_all(self):
        return self.db_session.query(GroupModel).all()

    def get_by_id(self, group_id: int):
        return self.db_session.query(GroupModel).filter(GroupModel.id == group_id).first()

    def update(self, group_id: int, group: Group):
        db_group = self.get_by_id(group_id)
        if db_group:
            db_group.name = group.name
            self.db_session.commit()
        return db_group

    def delete(self, group_id: int):
        db_group = self.get_by_id(group_id)
        if db_group:
            self.db_session.delete(db_group)
            self.db_session.commit()
            return True
        return False