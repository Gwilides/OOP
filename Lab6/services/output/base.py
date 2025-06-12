from .abstract import AbstractOutputService


class ConsoleFileWriter(AbstractOutputService):
    def __init__(
            self,
            *,
            default_text: str = "",
            output_file: str = "output.txt",
    ):
        self._text = default_text
        self._output_file = output_file

        try:
            self._file = open(self._output_file, 'w',
                              encoding='utf-8')
        except OSError as e:
            raise RuntimeError(f"Failed to open {output_file}: {e}") from e

    def char(self, char: str) -> None:
        self._text += char
        print(char)
        self._file.write(f"{self._text}\n")
        self._file.flush()

    def message(self, message: str, need_write: bool = True) -> None:
        print(message)
        if need_write:
            self._file.write(f"{message}\n")
            self._file.flush()

    def remove_last_char(self) -> None:
        if not self._text:
            return
        self._text = self._text[:-1]
        print("undo")
        self._file.write(f"{self._text}\n")
        self._file.flush()

    def __del__(self):
        self._file.close()
