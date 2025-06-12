from abc import abstractmethod, ABC


class AbstractOutputService(ABC):
    @abstractmethod
    def char(self, char: str) -> None: ...

    @abstractmethod
    def message(self, message: str, *kwargs) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...
