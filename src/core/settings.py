from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables and .env file.
    """
    app_name: str
    debug: bool
    database_url: str
    geocode_url: str


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()