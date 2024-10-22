from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict
from messages.dao import MessagesDAO
from messages.schemas import MessageRead, MessageCreate
from users.dao import UsersDAO
from users.dependencies import get_current_user
from users.models import User
import asyncio
import logging

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="app/templates")


# Страница чата
@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    users_all = await UsersDAO.find_all()
    return templates.TemplateResponse(
        "chat.html", {"request": request, "user": user_data, "users_all": users_all}
    )


@router.get("/messages/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return (
        await MessagesDAO.get_messages_between_users(
            user_id_1=user_id, user_id_2=current_user.id
        )
        or []
    )


@router.post("/messages", response_model=MessageCreate)
async def send_message(
    message: MessageCreate, current_user: User = Depends(get_current_user)
):
    # Add new message to the database
    await MessagesDAO.add(
        from_user_id=current_user.id,
        text=message.content,
        to_user_id=message.recipient_id,
    )

    return {
        "to_user_id": message.recipient_id,
        "text": message.content,
        "status": "ok",
        "msg": "Message saved!",
    }
