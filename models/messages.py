from database.connection import Base
from sqlalchemy import JSON, Column, Integer, String, DateTime
"""from pydantic import BaseModel
from typing import Optional
from datetime import datetime"""


"""class Message(BaseModel):
    id: int
    from_user: int  # TODO сделать ссылку на юзера
    to_user: int
    chat_id: Optional[int] = None
    status: str
    was_sent_at: datetime
"""

class PMessages(Base):
    __tablename__ = "pmessages"

    id = Column(Integer, primary_key=True)
    #from user
    chat_id = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    was_sent_at = Column(DateTime)