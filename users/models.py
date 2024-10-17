from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database.connection import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    telegram: Mapped[str] = mapped_column(String, nullable=True)