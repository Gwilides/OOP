from abc import ABC, abstractmethod
from commands.base import Command
from commands.print import PrintCharCommand
from commands.volume import VolumeUpCommand, VolumeDownCommand
from commands.media import MediaPlayerCommand


class CommandFactory(ABC):
    @abstractmethod
    def create_command(self, command_type: str, key: str, output_service) -> Command:
        pass


class DefaultCommandFactory(CommandFactory):
    def __init__(self):
        self._command_registry: dict[str, type[Command]] = {
            "PrintCharCommand": PrintCharCommand,
            "VolumeUpCommand": VolumeUpCommand,
            "VolumeDownCommand": VolumeDownCommand,
            "MediaPlayerCommand": MediaPlayerCommand,
        }

    def create_command(self, command_type: str, key: str, output_service) -> Command:
        if command_type not in self._command_registry:
            raise ValueError(f"Unknown command type: {command_type}")

        command_class = self._command_registry[command_type]

        if command_type == "PrintCharCommand":
            char = key[0] if key else 'a'
            return command_class(char, output_service)
        else:
            return command_class(output_service)
