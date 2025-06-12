from collections import deque

from commands.base import Command
from commands.print import PrintCharCommand
from commands.volume import VolumeUpCommand, VolumeDownCommand
from commands.media import MediaPlayerCommand
from services.output.base import ConsoleFileWriter


class Keyboard:
    def __init__(self):
        self._output_service = ConsoleFileWriter()
        self._key_bindings: dict[str, Command] = {}

        self._undo_stack: deque[Command] = deque()
        self._redo_stack: deque[Command] = deque()

    def key_bind(self, key: str, command: Command) -> None:
        self._key_bindings[key] = command

    def press_key(self, key: str) -> None:
        if key in self._key_bindings:
            command = self._key_bindings[key]
            command.execute()
            self._undo_stack.append(command)
            self._redo_stack.clear()

    def undo(self) -> None:
        if self._undo_stack:
            command = self._undo_stack.pop()
            command.undo()
            self._redo_stack.append(command)

    def redo(self) -> None:
        if self._redo_stack:
            self._output_service.message("redo", need_write=False)
            command = self._redo_stack.pop()
            command.execute()
            self._undo_stack.append(command)

    def get_bindings_for_save(self) -> dict[str, str]:
        result = {}
        for key, command in self._key_bindings.items():
            result[key] = type(command).__name__
        return result

    def restore_bindings(self, bindings: dict[str, str]) -> None:
        for key, command_type in bindings.items():
            if command_type == "PrintCharCommand":
                char = key[0] if key else 'a'
                self.key_bind(key, PrintCharCommand(
                    char, self._output_service))
            elif command_type == "VolumeUpCommand":
                self.key_bind(key, VolumeUpCommand(self._output_service))
            elif command_type == "VolumeDownCommand":
                self.key_bind(key, VolumeDownCommand(self._output_service))
            elif command_type == "MediaPlayerCommand":
                self.key_bind(key, MediaPlayerCommand(self._output_service))
