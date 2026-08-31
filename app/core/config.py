from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # App General Settings
    APP_NAME: str = "Ecommerce AI Assistant"
    DEBUG: bool = True

    # Security / JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Databases Configurations
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    MONGODB_URL: str
    MONGODB_DB_NAME: str

    # Gemini AI Key
    GEMINI_API_KEY: str
    model : str

    # Helper Property: Auto-creates PostgreSQL Connection URI
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Pydantic Configuration to look for .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # .env me koi extra variable ho to use ignore karega crash krne ki bajaye
    )

# Ek single instance banate hain jo poori app me use hoga
settings = Settings()