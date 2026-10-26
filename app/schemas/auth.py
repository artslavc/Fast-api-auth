from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Логин пользователя")
    password: str = Field(..., min_length=1, description="Пароль пользователя")


class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str | None = None