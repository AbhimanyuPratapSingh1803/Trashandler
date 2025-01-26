from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

class Settings(BaseSettings):
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")

settings = Settings()