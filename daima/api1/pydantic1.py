from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    email: str

class Group(BaseModel):
    id: int
    name: str
    students: list[Student] = []
