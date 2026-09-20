from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from app.config import settings
import jwt 
from app.models import User




def get_db() -> Generator[Session, None , None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
DbSession = Annotated[Session , Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token : Annotated[str, Depends(oauth2_scheme)] , db: DbSession) -> User:
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Could not validate credentials", 
                              headers={"WWW-Authenticate": "Bearer"})
    try:
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITM
        )
        email : str | None = data.get("sub")
        if not email:
            raise exception
        

    except jwt.PyjwtError:
        raise exception
    
    statement = select(User).where(User.email == email)
    result = statement.scalar()
    
    if result is None:
        raise exception
    
    if not result.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User"
        )
    
    return User

CurrentUser = Annotated[User, Depends(get_current_user)]
    
    
    
        
    