from fastapi import APIRouter, HTTPException, status
import jwt
from datetime import datetime, timedelta, timezone

from app.schemas.auth import LoginRequest, LoginResponse
router = APIRouter(prefix="/auth", tags=["auth"])
# Конфигурация. В проде, понятное дело, лучше использовать переменные окружения, а также отдельно вынести.
SECRET_KEY = "random_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Заглушка, т.к. проект просто идет в портфолио, не стал подключать б/д
FAKE_USER = {
    "username": "admin",
    "password": "123123",
}


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest) -> LoginResponse:
    if (
        payload.username != FAKE_USER["username"]
        or payload.password != FAKE_USER["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
        )

    access_token = create_access_token(
        data={"sub": payload.username},
        expires_delta=timedelta(days=30)
    )

    return LoginResponse(
        success=True,
        message="Успешная авторизация",
        access_token=access_token
    )