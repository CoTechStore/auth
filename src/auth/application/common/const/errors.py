from typing import Final

APPLICATION_FORBIDDEN: Final[str] = "У пользователя нет доступа к этой операции."

INVALID_LOGIN_OR_PASSWORD: Final[str] = "Неверный логин или пароль."
INVALID_TOKEN: Final[str] = "Неверный токен."
INVALID_CREDENTIALS: Final[str] = "Неверные учетные данные."

UNAUTHORIZED: Final[str] = "Пользователь не авторизован."
UNAUTHENTICATED: Final[str] = "Пользователь не прошел проверку подлинности."
EXPIRED_SIGNATURE: Final[str] = (
    "Срок действия вашего токена истек. Пожалуйста, войдите в систему еще раз."
)
DECODE: Final[str] = (
    "Срок действия вашего токена истек. Пожалуйста, войдите в систему еще раз."
)
MISSION_REQUIRED_CLAIM: Final[str] = "В вашем токене нет обязательного поля."

USER_SESSION_NOT_FOUND: Final[str] = "Сессия пользователя не найдена."
USER_ALREADY_AUTHENTICATED: Final[str] = "Пользователь уже прошел проверку подлинности."
