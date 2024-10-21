from pydantic import BaseModel, EmailStr, Field, field_validator


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    password_check: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
    username: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    telegram: str = Field(..., min_length=5, max_length=33, description="Логин телеграм, в форме '@username'")

    @field_validator('telegram')
    def validate_telegram(cls, value):
        if not value.startswith('@'):
            raise ValueError("Telegram username must start with '@'")
        return value


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков")
