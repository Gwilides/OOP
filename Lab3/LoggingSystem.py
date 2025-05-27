from typing import Protocol, List
import re, socket
from datetime import datetime

class LogFilterProtocol(Protocol):
    def match(self, message: str) -> bool:
        ...

class LogHandlerProtocol(Protocol):
    def handle(self, message: str) -> None:
        ...

class SimpleLogFilter:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, message: str) -> bool:
        return self.pattern in message
    
class ReLogFilter:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, message: str) -> bool:
        return bool(self.pattern.search(message))

class FileHandler:
    def __init__(self, filename: str, append_mode: bool = True):
        self.filename = filename
        self.mode = 'a' if append_mode else 'w'
    
    def handle(self, message: str) -> None:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log = f"[{timestamp}] {message}\n"

        try:
            with open(f"./Logs/{self.filename}", self.mode, encoding="utf-8") as f:
                f.write(log)
                f.flush()
        except PermissionError:
            print(f"[FileHandler] ОШИБКА: Нет прав на запись в файл {self.filename}")
        except FileNotFoundError:
            print(f"[FileHandler] ОШИБКА: Путь к файлу {self.filename} не найден")

class SocketHandler:
    def __init__(self, host: str = 'localhost',
                 port: int = 12345,
                 timeout: int = 5,
                 connection_attempts: int = 3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.connection_attempts = connection_attempts
    
    def handle(self, message: str) -> None:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log = f"[{timestamp}] {message}\n"

        for attempt in range(1, self.connection_attempts + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.timeout)
                    s.connect((self.host, self.port))
                    s.send(log.encode('utf-8'))
                    return
            except socket.timeout:
                print(f"[SocketHandler] Попытка {attempt}/{self.connection_attempts}: Таймаут подключения к {self.host}:{self.port}")
            except socket.gaierror as e:
                print(f"[SocketHandler] Попытка {attempt}/{self.connection_attempts}: Ошибка разрешения имени {self.host}: {e}")

        print(f"[SocketHandler] ОШИБКА: Не удалось отправить лог после {self.connection_attempts} попыток")

class ConsoleHandler:
    def handle(self, message: str) -> None:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"[CONSOLE {timestamp}] {message}")

class SyslogHandler:
    def handle(self, message: str) -> None:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        print(f"[SYSLOG {timestamp}] {message}")

class Logger:
    def __init__(self,
                 filters: List[LogFilterProtocol] | None = None,
                 handlers: List[LogHandlerProtocol] | None = None):
        self.filters = filters or []
        self.handlers = handlers or []

    def log(self, message: str) -> None:
        if not any(filter.match(message) for filter in self.filters):
            return
        
        for handler in self.handlers:
            try:
                handler.handle(message)
            except Exception as e:
                print(f"Ошибка в обработчике {type(handler).__name__}: {e}")

if __name__ == "__main__":
    error_filter = SimpleLogFilter("ERROR")
    warning_filter = SimpleLogFilter("WARNING")
    date_filter = ReLogFilter(r'\d{2}.\d{2}.\d{3}')

    console_handler = ConsoleHandler()
    file_handler = FileHandler("Logs.log")
    socket_handler = SocketHandler("127.0.0.1", 8080)
    syslog_handler = SyslogHandler()
    logger = Logger(
            filters=[error_filter, warning_filter, date_filter],
            handlers=[console_handler, file_handler, socket_handler, syslog_handler]
        )

    test_messages = [
            "INFO: Приложение запущено успешно",
            "ERROR: Не удалось подключиться к базе данных",
            "WARNING: Низкий уровень памяти",
            "DEBUG: Выполняется запрос к API",
            "ERROR 05.05.2025: Критическая ошибка в модуле аутентификации",
            "SUCCESS: Операция завершена успешно",
            "WARNING: Превышен лимит запросов"
        ]

    for i, message in enumerate(test_messages, 1):
            print(f"\nТест {i}: {message}\n")
            logger.log(message)
            print("-" * 30)