import bcrypt

from auth.application.ports import PasswordVerify
from auth.application.ports.password_hasher import PasswordHasher


class BcryptPasswordImpl(PasswordHasher, PasswordVerify):
    def hash(self, password: str) -> bytes:
        """Хеширование пароля при регистрации."""
        salt = bcrypt.gensalt()
        password_bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)

    def verify(self, new_password: str, old_password: bytes) -> bool:
        """Сравнивает хэшированный пароль с паролем из БД."""
        return bcrypt.checkpw(
            password=new_password.encode(), hashed_password=old_password
        )
