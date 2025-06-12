from abc import abstractmethod, ABC


class AbstractOutputService(ABC):
    @abstractmethod
    def char(self, char: str) -> None: ...

    @abstractmethod
    def message(self, message: str, *args) -> None: ...

    @abstractmethod
    def remove_last_char(self) -> None: ...
