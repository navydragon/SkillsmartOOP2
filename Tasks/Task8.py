# Ковариативность пример

from typing import Generic, Iterator, TypeVar


class Animal:
    def make_sound(self):
        return "Звук животного"


class Cat(Animal):
    def make_sound(self):
        return "Мяу"


class Dog(Animal):
    def make_sound(self):
        return "Гав"


# Ковариантный тип для неизменяемых контейнеров
T_co = TypeVar("T_co", covariant=True)


class ImmutableList(Generic[T_co]):
    """Неизменяемый список - ковариантен по типу элементов"""

    def __init__(self, items: list[T_co]):
        self._items = list(items)

    def get(self, index: int) -> T_co:
        return self._items[index]

    def __iter__(self) -> Iterator[T_co]:
        return iter(self._items)


# Демонстрация ковариантности
def process_animals(animals: ImmutableList[Animal]):
    """Функция, работающая с любыми животными"""
    for animal in animals:
        print(animal.make_sound())


# Создаем списки
cats = ImmutableList([Cat(), Cat()])
dogs = ImmutableList([Dog(), Dog()])

# Благодаря ковариантности можем передать ImmutableList[Cat]
# туда, где ожидается ImmutableList[Animal]
process_animals(cats)  # Работает!
process_animals(dogs)  # Работает!


# Контрвариативность пример

from typing import Callable, Generic, TypeVar

# Контравариантный тип для потребителей данных
T_contra = TypeVar("T_contra", contravariant=True)


class DataProcessor(Generic[T_contra]):
    """Процессор данных - контравариантен по типу обрабатываемых данных"""

    def process(self, item: T_contra) -> None:
        pass


class AnimalProcessor(DataProcessor[Animal]):
    def process(self, animal: Animal) -> None:
        print(f"Обрабатываю животное: {animal.make_sound()}")


class CatProcessor(DataProcessor[Cat]):
    def process(self, cat: Cat) -> None:
        print(f"Обрабатываю кота: {cat.make_sound()}")


# Демонстрация контравариантности
def handle_cats(processor: DataProcessor[Cat], cats: list[Cat]):
    """Функция для обработки котов"""
    for cat in cats:
        processor.process(cat)


# Благодаря контравариантности можем использовать DataProcessor[Animal]
# там, где ожидается DataProcessor[Cat]
animal_processor = AnimalProcessor()
cat_processor = CatProcessor()
cats = [Cat(), Cat()]

handle_cats(animal_processor, cats)  # Работает! (контравариантность)
handle_cats(cat_processor, cats)  # Работает!
