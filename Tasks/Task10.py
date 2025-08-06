# В Python Декоратор @final работает только на уровне статической проверки
# типов, но не блокирует выполнение кода.

from typing import final


class Base:
    @final
    def important_method(self) -> None:
        """Этот метод не должен переопределяться"""
        print("Критически важная логика")

    def regular_method(self) -> None:
        """Этот метод можно переопределять"""
        print("Обычная логика")


class Derived(Base):
    def regular_method(self) -> None:
        """Переопределение разрешено"""
        print("Новая логика")

    def important_method(self) -> None:
        """Это вызовет ошибку при статической проверке"""
        print("Попытка переопределения")


if __name__ == "__main__":
    derived = Derived()
    derived.regular_method()
    derived.important_method()
