from datetime import datetime, timedelta, timezone
import jwt
from typing import Optional
import bcrypt
from app.config import settings


def hash_password(password : str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed

def verify_password(plain_password : str , hashed_password : str) -> bool:
    encoded_plain_pd = plain_password.encode("utf-8")
    encoded_hashed_pd = hashed_password.encode("utf-8")
    return bcrypt.checkpw(encoded_plain_pd, encoded_hashed_pd)


def create_access_token(data : dict, expires_delta : Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp" : expire})
    
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    return encode_jwt
