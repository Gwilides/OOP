from typing import Protocol, List, Any

class PropertyChangedListenerProtocol(Protocol):
    def on_property_changed(obj: Any, property_name) -> None:
        ...

class DataChangedProtocol(Protocol):
    def add_property_changed_listener(listener: PropertyChangedListenerProtocol):
        ...
    def remove_property_changed_listener(listener: PropertyChangedListenerProtocol):
        ...

class NotifyDataChanged(DataChangedProtocol):
    def __init__(self):
        self._listeners: List[PropertyChangedListenerProtocol] = []
        self._name = ""
        self._age = 0
        self._email = ""
    
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._listeners.append(listener)
    
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _property_changed(self, property_name: str) -> None:
        for listener in self._listeners:
            listener.on_property_changed(self, property_name)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        self._property_changed("name")
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = value
        self._property_changed("age")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        self._email = value
        self._property_changed("email")

class PropertyChangingListenerProtocol(Protocol):
    def on_property_changing(obj: Any, property_name, old_value, new_value) -> bool:
        ...

class DataChangingProtocol(Protocol):
    def add_property_changing_listener(listener: PropertyChangingListenerProtocol):
        ...
    def remove_property_changing_listener(listener: PropertyChangingListenerProtocol):
        ...

class NotifyDataChanging(DataChangingProtocol):
    def __init__(self):
        self._changing_listeners: List[PropertyChangingListenerProtocol] = []
        self._changed_listeners: List[PropertyChangedListenerProtocol] = []
        self._name = ""
        self._age = 0
        self._email = ""
    
    def add_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        self._changing_listeners.append(listener)
    
    def remove_property_changing_listener(self, listener: PropertyChangingListenerProtocol) -> None:
        if listener in self._changing_listeners:
            self._changing_listeners.remove(listener)
    
    def add_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        self._changed_listeners.append(listener)
    
    def remove_property_changed_listener(self, listener: PropertyChangedListenerProtocol) -> None:
        if listener in self._changed_listeners:
            self._changed_listeners.remove(listener)
    
    def _property_changing(self, property_name: str, old_value: Any, new_value: Any) -> bool:
        for listener in self._changing_listeners:
            if not listener.on_property_changing(self, property_name, old_value, new_value):
                return False
        return True
    
    def _property_changed(self, property_name: str) -> None:
        for listener in self._changed_listeners:
            listener.on_property_changed(self, property_name)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if self._property_changing("name", self._name, value):
            self._name = value
            self._property_changed("name")
        else:
            print(f"Изменение имени отклонено: '{value}'")
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if self._property_changing("age", self._age, value):
            self._age = value
            self._property_changed("age")
        else:
            print(f"Изменение возраста отклонено: {value}")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if self._property_changing("email", self._email, value):
            self._email = value
            self._property_changed("email")
        else:
            print(f"Изменение email отклонено: '{value}'")
    

class LoggingListener:
    def __init__(self, name: str):
        self.name = name
    
    def on_property_changed(self, obj: Any, property_name: str) -> None:
        current_value = getattr(obj, property_name)
        print(f"[{self.name}] Свойство '{property_name}' изменено на: {current_value}")

class NameValidator:
    def on_property_changing(self, obj: Any, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name == "name":
            if not isinstance(new_value, str) or len(new_value) < 2 or len(new_value) > 50:
                print(f"[Валидация имени] Недопустимое имя: '{new_value}'")
                return False
            print(f"[Валидация имени] Имя '{new_value}' прошло валидацию")
        return True

class AgeValidator:
    def on_property_changing(self, obj: Any, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name == "age":
            if not isinstance(new_value, int) or new_value < 0 or new_value > 200:
                print(f"[Валидация возраста] Недопустимый возраст: {new_value}")
                return False
            print(f"[Валидация возраста] Возраст {new_value} прошел валидацию")
        return True

class EmailValidator:
    def on_property_changing(self, obj: Any, property_name: str, old_value: Any, new_value: Any) -> bool:
        if property_name == "email":
            if not isinstance(new_value, str) or "@" not in new_value or "." not in new_value:
                print(f"[Валидация email] Недопустимый email: {new_value}")
                return False
            print(f"[Валидация email] Email '{new_value}' прошел валидацию")
        return True

if __name__ == "__main__":
    first_obj = NotifyDataChanged()
    second_obj = NotifyDataChanging()

    logger1 = LoggingListener("Логгер-1")
    logger2 = LoggingListener("Логгер-2")

    name_validator = NameValidator()
    age_validator = AgeValidator()
    email_validator = EmailValidator()

    print("-" * 50, "\n")
    first_obj.add_property_changed_listener(logger1)

    first_obj.name = "Иван"
    first_obj.age = 25
    first_obj.email = "ivan@example.com"
    print("-" * 50, "\n")

    second_obj.add_property_changed_listener(logger2)
    second_obj.add_property_changing_listener(name_validator)
    second_obj.add_property_changing_listener(age_validator)
    second_obj.add_property_changing_listener(email_validator)

    second_obj.name = "Мария"
    second_obj.age = 30
    second_obj.email = "maria@company.com"
    print("-" * 50, "\n")
    
    second_obj.name = "А"
    second_obj.age = -5
    second_obj.age = 200
    second_obj.email = "неправильный_email"