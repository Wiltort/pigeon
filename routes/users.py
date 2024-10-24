from fastapi import APIRouter, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routes.exceptions import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    PasswordMismatchException,
    IncorrectTelegramException,
)
from users.auth import get_password_hash, authenticate_user, create_access_token
from users.dao import UsersDAO
from users.schemas import SUserRegister, SUserAuth
from routes.chat import notify_all_users
from database.connection import async_session_maker
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory='templates')


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("Пароли не совпадают")
    if user_data.telegram[0] != "@":
        raise IncorrectTelegramException()
    hashed_password = get_password_hash(user_data.password)
    async with async_session_maker() as session:
        async with session.begin():
            new_user = User(
                username=user_data.username,
                email=user_data.email,
                password=hashed_password,
                telegram=user_data.telegram,
            )
            session.add(new_user)
            try:
                await session.commit()
                # Refresh the instance to ensure it's up-to-date
                await session.refresh(new_user)
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
    new_user_data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'telegram': new_user.telegram
    }
    await notify_all_users({'event': 'new_user', 'user': new_user_data})
    return {"message": "Вы успешно зарегистрированы!"}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": None,
        "message": "Авторизация успешна!",
    }


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}


@router.get("/", response_class=HTMLResponse, summary="Страница авторизации")
async def get_categories(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

