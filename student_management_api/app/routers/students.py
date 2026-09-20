from fastapi import APIRouter, status, HTTPException, Query
from app.schemas import StudentCreate, StudentUpdate, StudentResponse
from app.services import student_service
from app.dependencies import DbSession,CurrentUser



router = APIRouter(prefix='/students', tags=['Students'])

@router.get('/', response_model=list[StudentResponse])
def get_all_students(db : DbSession, skip: int = Query(0, ge=0, description="Number of records to skip"),
                     limit: int = Query(10,ge=1, le=100,description="Max number of records to return"),
                     department: str | None = Query(None, description="Filter by department"),
                     search : str | None = Query(None, description="Search by name or roll number")):
    
    students = student_service.get_all_student(db, skip=skip, limit=limit, department=department, search=search)
    
    return students

@router.get('/{student_id}', response_model=StudentResponse)
def get_by_student_id(student_id : int, db : DbSession):
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    
    return student

@router.post('/' , response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def student_update(student : StudentCreate, db : DbSession , current_user : CurrentUser):
    students = student_service.create_student(db, student)
    return students   

@router.patch('/{student_id}' , response_model= StudentResponse)
def patch_update(student_id : int , student_update : StudentUpdate, db : DbSession, current_user : CurrentUser ):
    student = student_service.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student not found")
    
    updated_student = student_service.update_student(db, student, student_update)
    return updated_student
    
@router.delete('/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id : int, db : DbSession,current_user : CurrentUser):
    student = student_service.get_student_by_id(db, student_id)
    
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    student_service.delete_student(db, student)
    return None

        

        
