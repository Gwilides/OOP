from commands.base import Command
from services.output.abstract import AbstractOutputService


class PrintCharCommand(Command):
    def __init__(self, char: str, output_service: AbstractOutputService):
        self._char = char
        self._output_service = output_service

    def execute(self) -> None:
        self._output_service.char(self._char)

    def undo(self) -> None:
        self._output_service.remove_last_char()
