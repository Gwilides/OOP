from commands.base import Command
from services.output.abstract import AbstractOutputService


class MediaPlayerCommand(Command):
    def __init__(self, output_service: AbstractOutputService):
        self._output_service = output_service

    def execute(self) -> None:
        self._output_service.message("media player launched")

    def undo(self):
        self._output_service.message("media player closed")
