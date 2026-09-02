from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://postgres:tu_password_segura@localhost:5432/inmobiliaria_db'
    cors_origins: str = 'http://localhost:4200'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
