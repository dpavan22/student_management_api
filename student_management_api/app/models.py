from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from app.database import Base 


class User(Base):
    __tablename__ = "Users"
    
    id : Mapped[int] = mapped_column(primary_key=True, index=True)
    email : Mapped[str] = mapped_column(unique=True,index=True,nullable=False)
    hashed_password : Mapped[str] = mapped_column(nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())
    
class Student(Base):
    __tablename__ = "students"
    
    id : Mapped[int] = mapped_column(primary_key=True,index=True)
    full_name : Mapped[str] = mapped_column(nullable=False)
    email : Mapped[str] = mapped_column(index=True, nullable=False)
    age : Mapped[int] = mapped_column(nullable=False)
    department : Mapped[str] = mapped_column(nullable = False)
    roll_number : Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at : Mapped[Optional[datetime]] = mapped_column(onupdate=func.now(), nullable=True)
       
    
    
    

    
    
    
    
  
    