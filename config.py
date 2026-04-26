from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    spring_data_mongodb_uri: str = "mongodb://localhost:27017" # using fallback
    mongodb_database: str = "recipe-app"
    port: int = 8080
    gemini_api_key: Optional[str] = None
    jwt_secret: str = "your_super_secret_jwt_key_that_is_at_least_32_characters_long"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 60 * 24 # 24 hours

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
