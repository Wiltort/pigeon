from database.connection import Base
from sqlalchemy import Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped
from users.models import User

class PMessages(Base):
    __tablename__ = "pmessages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    from_user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    to_user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    text: Mapped[str] = mapped_column(Text)
    was_sent_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

