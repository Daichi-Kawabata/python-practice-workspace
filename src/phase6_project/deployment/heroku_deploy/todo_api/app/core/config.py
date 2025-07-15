from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT設定
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # データベース設定
    DATABASE_URL: str = "sqlite:///./todo_api.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
