from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES: str
    
    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    
    SENDGRID_API_KEY: str
    SENDGRID_FROM_EMAIL: str
    
    class Config:
        env_file = '.env'

settings = Settings()