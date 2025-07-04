from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, LoginRequest, TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.crud.user import get_user_by_email, create_user, get_user_by_id
from app.core.security import verify_password, create_access_token, create_email_verification_token, verify_email_token
from app.core.security import create_password_reset_token, verify_password_reset_token, get_password_hash
from app.core.email import send_verification_email, send_password_reset_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# response_model -> uses the schema model to sanitize the returned data
# Session=Depends(get_db) -> injects db session 
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email is already registered")
    
    new_user = create_user(db, user_data)
    
    token = create_email_verification_token(str(new_user.id))
    send_verification_email(new_user.email, token)
    
    return new_user



@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user_id = verify_email_token(token)
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email is already verified")
    user.is_verified = True
    db.commit()
    return {"message": "Email successfully verified"}



@router.post("/login", response_model=TokenResponse)
def login(login_credential: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, str(login_credential.email))
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="This account is not registered. Please register first.")
        
    verify_pass = verify_password(login_credential.password, user.hashed_password)
    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid Credentials")
        
        
    # checking if the email is verified     
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Email not verified")
        
    token = create_access_token({"sub": str(user.id)})
    # token type is already set to bearer. just passing the access_token
    return TokenResponse(access_token=token)



@router.post("/forgot-password")
def forgot_password(forgot_password_request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, forgot_password_request.email)
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    token = create_password_reset_token(str(user.email))
    send_password_reset_email(to_email=user.email, token=token)
    return {"message": "Password reset email sent. Please check you email"}


@router.post("/reset-password")
def reset_password(reset_password_request: ResetPasswordRequest, db: Session= Depends(get_db)):
    email = verify_password_reset_token(reset_password_request.token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid token")
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    hashed_password = get_password_hash(reset_password_request.new_password)
    user.hashed_password = hashed_password
    db.commit()
    
    return {"message": "Password reset successful"}