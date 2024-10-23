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
from notice_bot.tasks import send_telegram_notification

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="templates")


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
        await MessagesDAO.get_history(user_id_1=user_id, user_id_2=current_user.id)
        or []
    )


# Активные WebSocket-подключения: {user_id: websocket}
active_connections: Dict[int, WebSocket] = {}


# Функция для отправки сообщения пользователю, если он подключен
async def notify_user(user_id: int, message: dict):
    """Отправить сообщение пользователю, если он подключен."""
    if user_id in active_connections:
        websocket = active_connections[user_id]
        # Отправляем сообщение в формате JSON
        await websocket.send_json(message)
    else:
        user = await UsersDAO.find_one_or_none(id=user_id)
        if user and user.telegram:
            send_telegram_notification.delay(user.telegram, message.text)



async def notify_all_users(message: dict):
    """Notify all connected users about a new user registration."""
    for websocket in active_connections.values():
        await websocket.send_json(message)


# WebSocket эндпоинт для соединений
@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    # Принимаем WebSocket-соединение
    await websocket.accept()
    # Сохраняем активное соединение для пользователя
    active_connections[user_id] = websocket
    try:
        while True:
            # Просто поддерживаем соединение активным (1 секунда паузы)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        # Удаляем пользователя из активных соединений при отключении
        active_connections.pop(user_id, None)


@router.post("/messages", response_model=MessageCreate)
async def send_message(
    message: MessageCreate, current_user: User = Depends(get_current_user)
):
    # Add new message to the database
    await MessagesDAO.add(
        from_user_id=current_user.id,
        text=message.text,
        to_user_id=message.to_user_id,
    )
    message_data = {
        "from_user_id": current_user.id,
        "to_user_id": message.to_user_id,
        "text": message.text,
    }
    await notify_user(
        message.to_user_id, {"event": "new_message", "message": message_data}
    )
    await notify_user(
        current_user.id, {"event": "new_message", "message": message_data}
    )
    return {
        "to_user_id": message.to_user_id,
        "text": message.text,
        "status": "ok",
        "msg": "Message saved!",
    }
