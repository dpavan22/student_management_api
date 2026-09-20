from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email : EmailStr
    

class UserCreate(UserBase):
    password : str = Field(min_length= 8 , max_length= 30)

class UserResponse(UserBase):
    id : int 
    is_active : bool
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)
    

class StudentBase(BaseModel):
    full_name : str = Field(min_length=2, max_length=100)
    email : EmailStr
    age : int = Field(ge=16, le=100)
    department : str = Field(min_length=2, max_length=50)
    roll_number : str = Field(min_length=3, max_length=20)
    

class StudentCreate(StudentBase):
    pass 

class StudentUpdate(BaseModel):
    full_name : Optional[str] = None
    email : Optional[str] = None
    age : Optional[int] = None
    department : Optional[str] = None
    roll_number : Optional[str] = None
    is_active : Optional[bool] = None
    
class StudentResponse(StudentBase):
    id : int 
    is_active : bool
    created_at : datetime
    updated_at : Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
    