from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = 'postgresql+asyncpg://nido:nido_dev@localhost:5432/nido_capital'
    cors_origins: str = 'http://localhost:4200'
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
