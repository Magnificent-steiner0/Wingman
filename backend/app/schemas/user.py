from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime, timezone


# schemas for user registration
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_oauth_user: bool
    created_at: datetime
    
    class Config:
        orm_modde=True
             
class UserInDB(UserOut):
    hashed_password: str



# schemas for user login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
# schemas for forgot password
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    