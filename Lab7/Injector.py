from abc import ABC, abstractmethod
from contextlib import contextmanager
from enum import Enum
from inspect import signature, isclass
from typing import Any, Optional, Callable, Union


class LifeStyle(Enum):
    PER_REQUEST = 'PerRequest'
    SCOPED = 'Scoped'
    SINGLETON = 'Singleton'


class Injector:
    def __init__(self):
        self._registrations: dict[
            type, 
            tuple[Union[type, Callable], LifeStyle, dict]
            ] = {}
        self._singletons: dict[type, Any] = {}
        self._scopes: Optional[dict[type, Any]] = None

    def register(
            self,
            interface_type: type,
            class_type: Union[type, Callable],
            life_circle: LifeStyle = LifeStyle.PER_REQUEST,
            params: Optional[dict] = None
    ):
        self._registrations[interface_type] = (class_type, life_circle, params or {})

    def get_instance(self, interface_type: type) -> Any:
        realization, life_circle, params = self._registrations[interface_type]

        if life_circle == LifeStyle.SINGLETON:
            if interface_type not in self._singletons:
                self._singletons[interface_type] = self._build(realization, params)
            return self._singletons[interface_type]

        if life_circle == LifeStyle.SCOPED:
            if self._scopes is None:
                raise RuntimeError('No active scope')
            if interface_type not in self._scopes:
                self._scopes[interface_type] = self._build(realization, params)
            return self._scopes[interface_type]

        return self._build(realization, params)

    def _build(self, realization: Union[type, Callable], params: dict) -> Any:
        if callable(realization) and not isclass(realization):
            instance = realization()
        else:
            constructor_params = {}
            sig = signature(realization.__init__)
            for name, param in sig.parameters.items():
                if param.annotation in self._registrations:
                    constructor_params[name] = self.get_instance(param.annotation)
            instance = realization(**constructor_params)

        for key, value in params.items():
            setattr(instance, key, value)

        return instance

    @contextmanager
    def create_scope(self):
        previous = self._scopes
        self._scopes = {}
        try:
            yield
        finally:
            self._scopes = previous


# интерфейсы
class Interface1(ABC):
    @abstractmethod
    def do_class1(self) -> str:
        pass


class Interface2(ABC):
    @abstractmethod
    def do_class2(self) -> str:
        pass


class Interface3(ABC):
    @abstractmethod
    def do_c(self) -> str:
        pass


# реализации
class Class1Debug(Interface1):
    def do_class1(self) -> str:
        return 'Class1 debug'


class Class1Release(Interface1):
    def do_class1(self) -> str:
        return 'Class1 release'


class Class2Debug(Interface2):
    def __init__(self, class1_service: Interface1):
        self._class1 = class1_service

    def do_class2(self) -> str:
        return f'Class2 debug uses {self._class1.do_class1()}'


class Class2Release(Interface2):
    def __init__(self, class1_service: Interface1):
        self._class1 = class1_service

    def do_class2(self) -> str:
        return f'Class2 release uses {self._class1.do_class1()}'


class Class3Debug(Interface3):
    def __init__(self, class2_service: Interface2):
        self._class2 = class2_service

    def do_c(self) -> str:
        return f'Class3 debug uses {self._class2.do_class2()}'


class Class3Release(Interface3):
    def __init__(self, class2_service: Interface2):
        self._class2 = class2_service

    def do_c(self) -> str:
        return f'Class3 release uses {self._class2.do_class2()}'

def main():
    # Конфигурация DEBUG
    debug_injector = Injector()
    debug_injector.register(Interface1, Class1Debug, LifeStyle.PER_REQUEST, {"debug_mode": True})
    debug_injector.register(Interface2, Class2Debug, LifeStyle.SINGLETON)
    debug_injector.register(Interface3, 
                        lambda: Class3Debug(debug_injector.get_instance(Interface2)), 
                        LifeStyle.SINGLETON)

    # Конфигурация RELEASE
    release_injector = Injector()
    release_injector.register(Interface1, Class1Release, LifeStyle.SINGLETON)
    release_injector.register(Interface2, Class2Release, LifeStyle.SCOPED)
    release_injector.register(Interface3, Class3Release, LifeStyle.PER_REQUEST)

    print("=== DEBUG CONFIG ===")
    
    singleton1 = debug_injector.get_instance(Interface3)
    singleton2 = debug_injector.get_instance(Interface3)
    print(f"Singleton equality: {singleton1 is singleton2}")
    
    per_req1 = debug_injector.get_instance(Interface1)
    per_req2 = debug_injector.get_instance(Interface1)
    if hasattr(per_req1, 'debug_mode'):
        print(f"debug_mode of per_req1: {per_req1.debug_mode}")
    print(f"PerRequest equality: {per_req1 is per_req2}")
    
    print(singleton1.do_c())

    print("\n=== RELEASE CONFIG ===")
    
    with release_injector.create_scope():
        scoped1 = release_injector.get_instance(Interface2)
        scoped2 = release_injector.get_instance(Interface2)
        print(f"Scoped equality: {scoped1 is scoped2}")
        
        per_req = release_injector.get_instance(Interface3)
        print(per_req.do_c())
        with release_injector.create_scope():
            new_scoped = release_injector.get_instance(Interface2)
            print(f"Is new scoped different: {scoped1 is not new_scoped}")
        

if __name__ == "__main__":
    main()