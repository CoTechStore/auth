from typing import Final

EXTENDED_FORBIDDEN: Final[str] = "Водителю нельзя назначить расширенную роль."

EMPTY_LOGIN: Final[str] = "Логин пользователя не должен быть пустым."
EMPTY_PASSWORD: Final[str] = "Пароль не должен быть пустым."

TOO_SHORT_LOGIN: Final[str] = "Логин пользователя не может быть короче 5 символов."
TOO_SHORT_PASSWORD: Final[str] = "Пароль не может быть короче 8 символов."

TOO_LONG_LOGIN: Final[str] = "Логин пользователя не может быть длиннее 30 символов."
TOO_LONG_PASSWORD: Final[str] = "Пароль не может быть длиннее 50 символов."

WRONG_LOGIN_FORMAT: Final[str] = "Логин введен некорректно."
WRONG_PASSWORD_FORMAT: Final[str] = (
    "Пароль должен содержать, только допустимые символы, латинские "
    "буквы Aa-Zz, хотя бы одну цифру и один специальный символ."
)
