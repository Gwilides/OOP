import json
import logging
from typing import Sequence, Type
from pathlib import Path


class DataRepository[T]:
    def __init__(self, filename: str, model_class: Type[T]):
        self._filename = Path(filename)
        self._model_class = model_class
        self._datas: list[T] = []
        self._load()

    def _load(self):
        if self._filename.exists():
            try:
                with open(self._filename, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                    self._datas = [self._model_class(**data) for data in raw]
            except Exception as e:
                logging.error(f'Error on reading file: {e}')

    def _save(self):
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(
                [data.__dict__ for data in self._datas],
                f,
                indent=2,
                ensure_ascii=False
            )

    def get_all(self) -> Sequence[T]:
        return sorted(self._datas, key=lambda data: data.name)

    def get_by_id(self, id: int) -> T | None:
        for data in self._datas:
            if data.id == id:
                return data
        return None

    def add(self, item: T) -> None:
        if any(user.id == item.id for user in self._datas):
            raise ValueError(f"User with ID {item.id} already exists")
        self._datas.append(item)
        self._save()

    def update(self, item: T) -> None:
        for i, data in enumerate(self._datas):
            if data.id == item.id:
                self._datas[i] = item
                self._save()
                return

    def delete(self, item: T) -> None:
        self._datas = [data for data in self._datas if data.id != item.id]
        self._save()
