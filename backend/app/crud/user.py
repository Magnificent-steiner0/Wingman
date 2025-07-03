from sqlalchemy.orm import Session
from app.db.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_email(db: Session, email:str)->User|None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, id: str)->User|None:
    return db.query(User).filter(User.id==id).first()


def create_user(db:Session, user:UserCreate)->User:
    hashed_password = get_password_hash(user.password)
    
    db_user = User(
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user