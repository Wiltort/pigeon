from celery import Celery
from aiogram import Bot, Dispatcher, Router
from config import get_tg_token
from aiogram.types import Message
from aiogram.filters import Command

import sqlite3


celery_app = Celery("tasks", broker="redis://localhost:6379/0")

TELEGRAM_BOT_TOKEN = get_tg_token()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
router = Router()
dp = Dispatcher()

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE
    )
"""
)
conn.commit()

async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username)
    )
    conn.commit()

    await message.reply("Ваши данные сохранены.")

router.message.register(start_command, Command(commands=["start"]))
dp.include_router(router)


def get_user_id_by_username(username):
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None


@celery_app.task
async def send_telegram_notification(username: str, message: str):
    """Послать юзеру сообщение в телеграм по его логину."""
    user_id = get_user_id_by_username(username=username[1:])
    await bot.send_message(chat_id=user_id, text=message)
