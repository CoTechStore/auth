from abc import ABC, abstractmethod


class PasswordVerify(ABC):
    @abstractmethod
    def verify(self, password: str, hash_password: bytes) -> bool: ...
