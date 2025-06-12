from commands.base import Command
from services.output.abstract import AbstractOutputService


class VolumeUpCommand(Command):
    def __init__(self, output_service: AbstractOutputService):
        self._output_service = output_service

    def execute(self) -> None:
        self._output_service.message("volume increased +20%")

    def undo(self) -> None:
        self._output_service.message("volume decreased -20%")


class VolumeDownCommand(Command):
    def __init__(self, output_service: AbstractOutputService):
        self._output_service = output_service

    def execute(self) -> None:
        self._output_service.message("volume decreased -20%")

    def undo(self) -> None:
        self._output_service.message("volume increased +20%")
