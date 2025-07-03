from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Union
from app.core.config import settings


# deprecated="auto" -> means if some better algo is added (e.g, argon2)
# consider bcrypt as deprecated and rehash old passwords auomatically
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# returns the hashed password
def get_password_hash(password: str)->str:
    return pwd_context.hash(password)


# it will verify the login password with the hashed password in DB
def verify_password(plain_password: str, hashed_password: str)->bool:
    return pwd_context.verify(plain_password, hashed_password)


# jwt config 
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.JWT_ACCESS_TOKEN_EXPIRES)

# expires_delta -> can be either timedelta object or None. default value is None
def create_access_token(data: dict, expires_delta: Union[timedelta, None]=None):
    # the data which is to be encoded is copied first. dict is passed by reference 
    # and we dont want to mutate the original data
    to_encode = data.copy()
    # if the expires_delta is not given explicitly then the ACCESS_TOKEN_EXPIRE_MINUTES will be used as default
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def create_email_verification_token(user_id: str):
    expire = datetime.now(timezone.utc)+timedelta(minutes=5)
    payload = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_email_token(token:str)->str:
    try:
        payload=jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    
    