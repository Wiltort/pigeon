from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from decouple import config


db_host = config("DB_HOST")
db_port = config("DB_PORT")
db_user = config("DB_USER")
db_pass = config("DB_PASS")
db_name = config("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession,
                                   expire_on_commit=False)


class Base(DeclarativeBase):
    pass
