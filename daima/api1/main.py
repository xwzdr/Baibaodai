from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic1 import Student, Group
from service import StudentService, GroupService
from database import get_db
from sql import StudentRepository, GroupRepository
import uvicorn
from fastapi import HTTPException

app = FastAPI()

if __name__=='__main__':
     uvicorn.run("main:app",host='127.0.0.1',port=8000,reload=True,workers=1)

@app.post("/students", response_model=Student)
def create_student(student: Student, db: Session = Depends(get_db)):
    student_service = StudentService(StudentRepository(db))
    return student_service.create_student(student)

@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student_service = StudentService(StudentRepository(db))
    student = student_service.get_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student, db: Session = Depends(get_db)):
    student_service = StudentService(StudentRepository(db))
    updated_student = student_service.update_student(student_id, student)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_service = StudentService(StudentRepository(db))
    success = student_service.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"detail": "Student deleted"}

@app.get("/students/", response_model=list[Student])
def list_students(db: Session = Depends(get_db)):
    student_service = StudentService(StudentRepository(db))
    return student_service.list_students()

# Class Related Routing
@app.post("/groups", response_model=Group)
def create_group(group: Group, db: Session = Depends(get_db)):
    group_service = GroupService(GroupRepository(db))
    return group_service.create_group(group)

@app.get("/groups/{group_id}", response_model=Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(GroupRepository(db))
    group = group_service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.put("/groups/{group_id}", response_model=Group)
def update_group(group_id: int, group: Group, db: Session = Depends(get_db)):
    group_service = GroupService(GroupRepository(db))
    updated_group = group_service.update_group(group_id, group)
    if not updated_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated_group

@app.delete("/groups/{group_id}", response_model=dict)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group_service = GroupService(GroupRepository(db))
    success = group_service.delete_group(group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"detail": "Group deleted"}

@app.get("/groups/", response_model=list[Group])
def list_groups(db: Session = Depends(get_db)):
    group_service = GroupService(GroupRepository(db))
    return group_service.list_groups()
