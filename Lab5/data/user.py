from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    name: str
    login: str
    password: str = field(repr=False)
    email: str | None = None
    address: str | None = None

    def __lt__(self, other: 'User') -> bool:
        return self.name < other.name