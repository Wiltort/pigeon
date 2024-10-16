from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    id: int
    from_user: int  # TODO сделать ссылку на юзера
    to_user: int
    chat_id: Optional[int] = None
    status: str
    was_sent_at: datetime

