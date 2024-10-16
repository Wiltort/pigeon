from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


#DB_HOST = "localhost"
#DB_PORT = 5432
#DB_USER = "postgres"
#DB_PASS = "postgres"
#DB_NAME = "pigeon"

DATABASE_URL = f"postgresql+asyncpg"