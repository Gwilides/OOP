from typing import Protocol

from data.user import User
from .data import DataRepositoryProtocol

class UserRepositoryProtocol(DataRepositoryProtocol[User], Protocol):
    def get_by_login(self, login: str) -> User | None: ...