import json
import os

from virtual_keyboard import Keyboard


class KeyboardStateSaver:
    def __init__(self, filepath: str = "keyboard_bindings.json"):
        self._filepath = filepath

    def save_state(self, keyboard: Keyboard) -> None:
        try:
            data = keyboard.get_bindings_for_save()
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Состояние сохранено в {self._filepath}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def load_state(self) -> dict[str, str] | None:
        if not os.path.exists(self._filepath):
            return None

        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Состояние загружено из {self._filepath}")
            return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Ошибка загрузки: {e}")
            return None
