
### 1. Наследование вариаций 

**Функциональная вариация** — переопределение логики метода без изменения сигнатуры:

```python
class Human:
    def greet(self):
        print("Привет!")

class Russian(Human):
    def greet(self):
        print("Здравствуйте!")  # Изменилась только логика
```

**Вариация типа** — изменение сигнатуры метода (перегрузка аргументов):

```python
class Human:
    def say(self, message):
        print(f"Human says: {message}")

class AdvancedHuman(Human):
    # Сигнатура отличается (добавлен параметр times)
    def say(self, message, times=1):
        for _ in range(times):
            print(f"AdvancedHuman says: {message}")
```


### 2. Наследование с конкретизацией (reification inheritance)

Базовый класс содержит абстрактный метод, а подкласс реализует его:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def voice(self):
        pass

class Cat(Animal):
    def voice(self):
        print("Мяу")

class Dog(Animal):
    def voice(self):
        print("Гав")
```


### 3. Структурное наследование

```python
class Car:
    def __init__(self, model, year):
        self.model = model
        self.year = year

class ComparableMixin:
    def __eq__(self, other):
        return self.year == other.year

    def __lt__(self, other):
        return self.year < other.year

class ComparableCar(Car, ComparableMixin):
    pass

car1 = ComparableCar("Volga", 1985)
car2 = ComparableCar("Lada", 1990)
print(car1 < car2)  # True — реализовано структурное наследование
```

