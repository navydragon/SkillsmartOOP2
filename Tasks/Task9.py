import copy
import json
import pickle
from abc import ABC, abstractmethod
from typing import Any as AnyType
from typing import Dict, Type, Union


class General(ABC):
    """
    Базовый абстрактный класс, содержащий фундаментальные операции.
    Закрыт для изменений и не допускает создания экземпляров.
    """

    def copy_to(self, target: "General") -> None:
        """
        Копирование содержимого текущего объекта в другой существующий объект.
        """
        if not isinstance(target, self.__class__):
            raise TypeError(f"Cannot copy to object of different type: {type(target)}")

        # Копируем все атрибуты объекта
        for attr_name in dir(self):
            if not attr_name.startswith("_") and not callable(getattr(self, attr_name)):
                try:
                    setattr(target, attr_name, getattr(self, attr_name))
                except AttributeError:
                    pass  # Пропускаем read-only атрибуты

    def deep_copy_to(self, target: "General") -> None:
        """
        Глубокое рекурсивное копирование содержимого объекта.
        """
        if not isinstance(target, self.__class__):
            raise TypeError(
                f"Cannot deep copy to object of different type: {type(target)}"
            )

        # Используем copy.deepcopy для глубокого копирования атрибутов
        for attr_name in dir(self):
            if not attr_name.startswith("_") and not callable(getattr(self, attr_name)):
                try:
                    setattr(target, attr_name, copy.deepcopy(getattr(self, attr_name)))
                except AttributeError:
                    pass  # Пропускаем read-only атрибуты

    def clone(self) -> "General":
        """
        Создание нового объекта и глубокое копирование в него исходного объекта.
        """
        # Создаем новый экземпляр того же класса
        cloned = self.__class__.__new__(self.__class__)

        # Глубоко копируем все атрибуты
        for attr_name, attr_value in self.__dict__.items():
            setattr(cloned, attr_name, copy.deepcopy(attr_value))

        return cloned

    def equals(self, other: "General") -> bool:
        """
        Сравнение объектов (поверхностное).
        """
        if not isinstance(other, self.__class__):
            return False

        return self.__dict__ == other.__dict__

    def deep_equals(self, other: "General") -> bool:
        """
        Глубокое сравнение объектов.
        """
        if not isinstance(other, self.__class__):
            return False

        # Сериализуем оба объекта для глубокого сравнения
        try:
            return self.serialize() == other.serialize()
        except:
            # Если сериализация не удалась, используем стандартное сравнение
            return self.__dict__ == other.__dict__

    def serialize(self) -> str:
        """
        Сериализация объекта в строковый формат.
        """
        try:
            # Пытаемся использовать JSON для читаемости
            serializable_dict = {}
            for key, value in self.__dict__.items():
                try:
                    json.dumps(value)  # Проверяем, можно ли сериализовать в JSON
                    serializable_dict[key] = value
                except (TypeError, ValueError):
                    # Если не получается JSON, используем строковое представление
                    serializable_dict[key] = str(value)

            return json.dumps(
                {"class": self.__class__.__name__, "data": serializable_dict},
                sort_keys=True,
                indent=2,
            )
        except:
            # Если JSON не работает, используем pickle в base64
            import base64

            return base64.b64encode(pickle.dumps(self)).decode("utf-8")

    @classmethod
    def deserialize(cls, data: str) -> "General":
        """
        Десериализация объекта из строкового формата.
        """
        try:
            # Пытаемся десериализовать из JSON
            obj_data = json.loads(data)
            if (
                isinstance(obj_data, dict)
                and "class" in obj_data
                and "data" in obj_data
            ):
                # Создаем новый экземпляр
                instance = cls.__new__(cls)
                # Восстанавливаем атрибуты
                for key, value in obj_data["data"].items():
                    setattr(instance, key, value)
                return instance
        except:
            pass

        try:
            # Пытаемся десериализовать из pickle
            import base64

            return pickle.loads(base64.b64decode(data.encode("utf-8")))
        except:
            raise ValueError("Cannot deserialize the provided data")

    def print_object(self) -> str:
        """
        Наглядное представление содержимого объекта в текстовом формате.
        """
        class_name = self.__class__.__name__
        attributes = []

        for attr_name, attr_value in self.__dict__.items():
            if not attr_name.startswith("_"):
                attributes.append(f"  {attr_name}: {repr(attr_value)}")

        if attributes:
            attrs_str = "\n" + "\n".join(attributes) + "\n"
        else:
            attrs_str = " (no attributes) "

        return f"{class_name} {{{attrs_str}}}"

    def is_type(self, target_type: Type) -> bool:
        """
        Проверка, является ли тип текущего объекта указанным типом.
        """
        return isinstance(self, target_type)

    def get_real_type(self) -> Type:
        """
        Получение реального типа объекта (класса, экземпляром которого он был создан).
        """
        return self.__class__

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.print_object()

    def __repr__(self) -> str:
        """Представление объекта для отладки."""
        return f"<{self.__class__.__name__} at {hex(id(self))}>"


class Any(General):
    """
    Прямой потомок General, открытый для модификации.
    Все новые классы проекта должны наследоваться от Any.
    """

    def __init__(self):
        """
        Базовый конструктор для Any.
        """
        super().__init__()
        self._created_at = None  # Можно добавлять общие компоненты

    def set_metadata(self, key: str, value: AnyType) -> None:
        """
        Пример метода, который может добавить архитектор проекта.
        Позволяет добавлять метаданные к объектам.
        """
        if not hasattr(self, "_metadata"):
            self._metadata = {}
        self._metadata[key] = value

    def get_metadata(self, key: str) -> AnyType:
        """
        Получение метаданных объекта.
        """
        if not hasattr(self, "_metadata"):
            return None
        return self._metadata.get(key)


# Пример использования
class Person(Any):
    """Пример класса, наследующегося от Any."""

    def __init__(self, name: str, age: int):
        super().__init__()
        self.name = name
        self.age = age


class Car(Any):
    """Еще один пример класса, наследующегося от Any."""

    def __init__(self, brand: str, model: str, year: int):
        super().__init__()
        self.brand = brand
        self.model = model
        self.year = year


# Демонстрация работы
if __name__ == "__main__":
    # Создаем объекты
    person1 = Person("Иван", 30)
    person2 = Person("Мария", 25)
    car = Car("Toyota", "Camry", 2020)

    print("=== Демонстрация базовых операций ===")

    # Печать объектов
    print("Объект person1:")
    print(person1.print_object())

    print("\nОбъект car:")
    print(car.print_object())

    # Проверка типов
    print(f"\nperson1 является Person: {person1.is_type(Person)}")
    print(f"person1 является Any: {person1.is_type(Any)}")
    print(f"person1 является General: {person1.is_type(General)}")
    print(f"Реальный тип person1: {person1.get_real_type()}")

    # Клонирование
    person1_clone = person1.clone()
    print(f"\nКлон person1: {person1_clone.print_object()}")
    print(f"person1 равен своему клону: {person1.equals(person1_clone)}")

    # Сериализация
    person1_serialized = person1.serialize()
    print(f"\nСериализованный person1:\n{person1_serialized}")

    # Десериализация
    person1_deserialized = Person.deserialize(person1_serialized)
    print(f"\nДесериализованный person1: {person1_deserialized.print_object()}")

    # Копирование
    person3 = Person("", 0)
    person1.copy_to(person3)
    print(f"\nПосле копирования person1 в person3: {person3.print_object()}")

    # Метаданные (пример расширения Any)
    person1.set_metadata("department", "IT")
    person1.set_metadata("salary", 50000)
    print(f"\nМетаданные person1 - department: {person1.get_metadata('department')}")
    print(f"Метаданные person1 - salary: {person1.get_metadata('salary')}")
