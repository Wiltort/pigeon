from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import get_database_data
from datetime import datetime
from sqlalchemy import func

db_data = get_database_data()

DATABASE_URL = f"postgresql+asyncpg://{db_data['db_user']}:{db_data['db_pass']}@{db_data['db_host']}:{db_data['db_port']}/{db_data['db_name']}"

engine = create_async_engine(DATABASE_URL)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
