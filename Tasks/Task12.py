import copy
import json
import pickle
from abc import ABC
from typing import Any as AnyType
from typing import Type, TypeVar, Union

# Определяем типовую переменную для работы с попытками присваивания
T = TypeVar("T")


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
            raise TypeError(
                f"Cannot copy to object of different type: {type(target)}"
            )
        # Копируем все атрибуты объекта
        for attr_name in dir(self):
            if (
                not attr_name.startswith("_")
                and not callable(getattr(self, attr_name))
            ):
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
            if (
                not attr_name.startswith("_")
                and not callable(getattr(self, attr_name))
            ):
                try:
                    setattr(
                        target, attr_name, copy.deepcopy(getattr(self, attr_name))
                    )
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
        except Exception:
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
        except Exception:
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

    @staticmethod
    def assignment_attempt(target_type: Type[T], source: "General") -> Union[T]:
        """
        Попытка присваивания: безопасное приведение типа.

        Args:
            target_type: Тип, к которому нужно привести объект
            source: Исходный объект

        Returns:
            Объект типа target_type или VoidInstance, если приведение невозможно
        """
        if source is None:
            return VoidInstance

        if isinstance(source, Void):
            return VoidInstance

        if isinstance(source, target_type):
            return source
        else:
            return VoidInstance

    @staticmethod
    def safe_cast(target_type: Type[T], source: "General") -> Union[T]:
        """
        Алиас для assignment_attempt для более понятного использования.
        """
        return General.assignment_attempt(target_type, source)

    def try_as(self, target_type: Type[T]) -> Union[T]:
        """
        Экземплярный метод для попытки приведения текущего объекта к указанному типу.

        Args:
            target_type: Тип, к которому нужно привести объект

        Returns:
            Объект типа target_type или VoidInstance
        """
        return General.assignment_attempt(target_type, self)

    def is_void(self) -> bool:
        """
        Проверка, является ли объект экземпляром Void.
        """
        return isinstance(self, Void)

    @staticmethod
    def is_void_value(obj: AnyType) -> bool:
        """
        Статический метод для проверки, является ли значение Void.
        """
        return isinstance(obj, Void)

    def safe_serialize(self) -> Union[str]:
        """
        Безопасная сериализация с попыткой присваивания.
        """
        try:
            return self.serialize()
        except:
            return VoidInstance

    @classmethod
    def safe_deserialize(cls, data: str) -> Union["General"]:
        """
        Безопасная десериализация с попыткой присваивания.
        """
        try:
            return cls.deserialize(data)
        except:
            return VoidInstance




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

        self._metadata = {}
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

    def safe_set_metadata(self, key: str, value: AnyType) -> bool:
        """
        Безопасная установка метаданных.

        Returns:
            True, если операция успешна, False - если произошла ошибка
        """
        try:
            self.set_metadata(key, value)
            return True
        except:
            return False

    def try_get_metadata(self, key: str, expected_type: Type[T]) -> Union[T]:
        """
        Попытка получения метаданных с проверкой типа.

        Args:
            key: Ключ метаданных
            expected_type: Ожидаемый тип значения

        Returns:
            Значение указанного типа или VoidInstance
        """
        value = self.get_metadata(key)
        if value is None:
            return VoidInstance

        return General.assignment_attempt(expected_type, value)

    def safe_copy_to(self, target: "General") -> bool:
        """
        Безопасное копирование с обработкой ошибок.

        Returns:
            True, если копирование успешно, False - если произошла ошибка
        """
        try:
            self.copy_to(target)
            return True
        except:
            return False

    def try_clone(self) -> Union["Any"]:
        """
        Попытка клонирования с безопасной обработкой ошибок.
        """
        try:
            return self.clone()
        except:
            return VoidInstance


class Person(Any):
    def __init__(self, name: str, age: int):
        super().__init__()
        self.name = name
        self.age = age


class Car(Any):
    def __init__(self, brand: str, model: str, year: int):
        super().__init__()
        self.brand = brand
        self.model = model
        self.year = year


class Void(Any):
    """
    Класс для представления пустого значения в системе типов.
    Замыкает иерархию снизу.
    """
    
    def __init__(self):
        # Не вызываем super().__init__(), чтобы избежать проблем с абстрактным классом
        pass
   
    def copy_to(self, target: 'General') -> None:
        """Void не может быть скопирован"""
        raise TypeError("Cannot copy Void object")
    
    def deep_copy_to(self, target: 'General') -> None:
        """Void не может быть глубоко скопирован"""
        raise TypeError("Cannot deep copy Void object")
    
    def clone(self) -> 'General':
        """Клонирование Void возвращает тот же экземпляр"""
        return VoidInstance
    
    def equals(self, other: 'General') -> bool:
        """Void равен только другому Void"""
        return isinstance(other, Void)
    
    def deep_equals(self, other: 'General') -> bool:
        """Глубокое сравнение для Void"""
        return isinstance(other, Void)
    
    def serialize(self) -> str:
        """Сериализация Void"""
        return '{"class": "Void", "data": null}'
    
    def print_object(self) -> str:
        """Печать Void"""
        return "Void { (empty) }"
    
    def __repr__(self):
        return "Void"
    
    def __str__(self):
        return "Void"
    
    def __bool__(self):
        return False


VoidInstance = Void()

if __name__ == "__main__":
    print("=== Демонстрация попытки присваивания ===")

    # Создаем объекты
    person = Person("Анна", 25)
    car = Car("Toyota", "Camry", 2020)

    # Базовые попытки присваивания
    print("1. Базовые попытки присваивания:")
    result1 = General.assignment_attempt(Person, person)
    result2 = General.assignment_attempt(Person, car)

    print(f"   Person <- Person: {result1}")
    print(f"   Person <- Car: {result2}")

    # Использование экземплярного метода
    print("\n2. Использование экземплярного метода:")
    person_as_person = person.try_as(Person)
    person_as_car = person.try_as(Car)

    print(f"   person.try_as(Person): {person_as_person}")
    print(f"   person.try_as(Car): {person_as_car}")

    # Безопасная работа с метаданными
    print("\n3. Безопасная работа с метаданными:")
    person.set_metadata("department", "IT")
    department = person.try_get_metadata("department", str)
    invalid_dept = person.try_get_metadata("nonexistent", str)

    print(f"   Существующий ключ: {department}")
    print(f"   Несуществующий ключ: {invalid_dept}")

    # Безопасное клонирование
    print("\n4. Безопасное клонирование:")
    clone_result = person.try_clone()
    void_clone = VoidInstance.try_clone()

    print(f"   Клонирование Person: {clone_result}")
    print(f"   Клонирование Void: {void_clone}")
