import asyncio
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.exceptions import TokenExpiredException, TokenNoFoundException
from routes.users import router as users_router
from routes.chat import router as chat_router
from notice_bot.tasks import dp, bot, init_db


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(users_router)
app.include_router(chat_router)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


async def start_bot():

    await dp.start_polling(bot)


if __name__ == "__main__":
    # Create a new event loop and run the app and bot concurrently
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    uvicorn.run(app, host="0.0.0.0", port=8000)