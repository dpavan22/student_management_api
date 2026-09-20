from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Student 
from app.schemas import StudentCreate, StudentUpdate


def get_all_student(db : Session,skip : int = 0, limit : int = 10, department : str | None =  None, search : str | None = None):
    statement = select(Student)
    if department:
        statement = statement.where(Student.department == department)
        
    if search:
        statement = statement.where(Student.full_name.icontains(search) | Student.roll_number.icontains(search))
    
    statement = statement.offset(skip).limit(limit)
        
    result = db.scalars(statement).all()
    return result 

def get_student_by_id(db : Session, student_id : int,):
    statement = select(Student).where(Student.id == student_id)
    result = db.scalar(statement)
    return result

def create_student(db : Session, student_in : StudentCreate):
    data = student_in.model_dump()
    db_student = Student(**data)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db : Session, db_student: Student, student_in : StudentUpdate):
    data = student_in.model_dump(exclude_unset=True)
    
    for key,value in data.items():
        setattr(db_student, key, value)
        
    
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db : Session , db_student : Student):
    db.delete(db_student)
    db.commit()
    db.refresh()
    
        