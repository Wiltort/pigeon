from celery import Celery
from aiogram import Bot, Dispatcher, Router
from config import get_tg_token
from aiogram.types import Message
from aiogram.filters import Command

import aiosqlite


celery_app = Celery("tasks", broker="redis://localhost:6379/0")

TELEGRAM_BOT_TOKEN = get_tg_token()
bot = Bot(token=TELEGRAM_BOT_TOKEN)
router = Router()
dp = Dispatcher()

async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE
            )
            """
        )
        await db.commit()


@router.message(Command=["start"])
async def start_command(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)", (user_id, username)
        )
        await db.commit()

    await message.reply("Ваши данные сохранены.")

# router.message.register(start_command, Command(commands=["start"]))
dp.include_router(router)


async def get_user_id_by_username(username):
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT id FROM users WHERE username = ?", (username,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else None


@celery_app.task
async def send_telegram_notification(username: str, message: str):
    """Послать юзеру сообщение в телеграм по его логину."""
    user_id = get_user_id_by_username(username=username[1:])
    await bot.send_message(chat_id=user_id, text=message)

