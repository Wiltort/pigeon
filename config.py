import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    TG_TOKEN: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_tg_token():
    return settings.TG_TOKEN


def get_database_data():
    return {
        "db_host": settings.DB_HOST,
        "db_port": settings.DB_PORT,
        "db_user": settings.DB_USER,
        "db_pass": settings.DB_PASS,
        "db_name": settings.DB_NAME,
    }
