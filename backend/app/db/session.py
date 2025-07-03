from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.orm import sessionmaker, Session
from collections.abc import Generator

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db()->Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()