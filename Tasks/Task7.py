from abc import ABC, abstractmethod


# Абстрактный базовый класс - определяет интерфейс
class Shape(ABC):
    """Базовый класс для всех геометрических фигур"""

    @abstractmethod
    def area(self):
        """Абстрактный метод для вычисления площади"""
        pass


# Конкретные реализации фигур
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius**2


class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height


# Калькулятор площадей - закрыт для изменений
class AreaCalculator:
    def __init__(self, shapes):
        self.shapes = shapes

    def calculate_total_area(self):
        """
        Этот метод не нужно изменять при добавлении новых фигур!
        Он работает с любыми объектами, реализующими интерфейс Shape
        """
        total_area = 0
        for shape in self.shapes:
            total_area += shape.area()  # Динамическое связывание!
        return total_area


# Добавляем новую фигуру БЕЗ изменения существующего кода
class Trapezoid(Shape):
    def __init__(self, base1, base2, height):
        self.base1 = base1
        self.base2 = base2
        self.height = height

    def area(self):
        return 0.5 * (self.base1 + self.base2) * self.height


# Использование
shapes = [
    Rectangle(5, 3),  # Площадь: 15
    Circle(4),  # Площадь: ≈50.27
    Triangle(6, 4),  # Площадь: 12
    Trapezoid(3, 7, 4),  # Площадь: 20
]

calculator = AreaCalculator(shapes)
print(f"Общая площадь: {calculator.calculate_total_area()}")
