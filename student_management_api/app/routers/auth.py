from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import DbSession
from app.models import User 
from app.schemas import UserResponse, Token , UserCreate
from app.utils.security import hash_password, verify_password, create_access_token
from sqlalchemy import select
from typing import Annotated


router = APIRouter(prefix='/auth', tags=['Authenication'])

@router.post('/register', response_model= UserResponse , status_code = status.HTTP_201_CREATED)
def register_node(user_in : UserCreate, db : DbSession):
    statement = select(User).where(User.email == user_in.email)
    result = db.scalars(statement).first()
    
    if result:
        raise HTTPException(status_code= 400, detail="Email already registered")
    
    hashed_pw = hash_password(user_in.password)
    db_user = User(email=user_in.email,
                   hashed_pwd=hashed_pw)
    
    db.commit()
    db.add(db_user)
    db.refresh()
    
    return db_user
    


@router.post('/login', response_model =Token)
def login_route(form_data : Annotated[OAuth2PasswordRequestForm ,Depends()], db : DbSession):
    statement = select(User).where(User.email == form_data.username)
    result = db.scalars(statement).first()
    
    if not result or not verify_password(form_data.password, result.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    
    token = create_access_token(data={'sub': result.email})
    return {
        'access_token': token,
        'token_type' : 'bearer'
    }
    
        
    
    
 
            
    