import bcrypt

from auth.application.ports import PasswordVerify


class BcryptPasswordImpl(PasswordVerify):
    def verify(self, new_password: str, old_password: bytes) -> bool:
        """Сравнивает хэшированный пароль с паролем из БД."""
        return bcrypt.checkpw(
            password=new_password.encode(), hashed_password=old_password
        )
