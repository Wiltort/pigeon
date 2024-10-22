from pydantic import BaseModel, Field
from datetime import datetime


class MessageRead(BaseModel):
    id: int = Field(..., description="Уникальный идентификатор сообщения")
    from_user_id: int = Field(..., description="ID отправителя сообщения")
    to_user_id: int = Field(..., description="ID получателя сообщения")
    text: str = Field(..., description="Содержимое сообщения")
    was_sent_at: datetime = Field(..., description="Дата отправления")


class MessageCreate(BaseModel):
    to_user_id: int = Field(..., description="ID получателя сообщения")
    text: str = Field(..., description="Содержимое сообщения")