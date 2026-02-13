from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "FastAPI Backend"
    ENV: str = "dev"
    API_V1_PREFIX: str = "/gti525/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SQLITE_DB_PATH: str = "comptage_velo.db"
    INPUT_DATA_DIR: Path = Path("public/input")


settings = Settings()
