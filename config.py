import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    SECRET_KEY: str
    ALGORITHM: str
    TG_TOKEN: str
    DATABASE_URL: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_auth_data():
    return {"secret_key": settings.SECRET_KEY, "algorithm": settings.ALGORITHM}


def get_tg_token():
    return settings.TG_TOKEN


def get_database_data():
    return settings.DATABASE_URL
