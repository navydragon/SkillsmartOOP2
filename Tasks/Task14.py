# ======= Общая система типов =======

class General:
    """
    Базовый абстрактный класс.
    Здесь только интерфейс для универсальности, логика — в потомках.
    """
    def __add__(self, other):
        raise NotImplementedError("Операция сложения не реализована для этого типа.")
    def __repr__(self):
        return f"{self.__class__.__name__}()"

class Any(General):
    """
    Базовый класс для пользовательских объектов. Может расширяться.
    """
    pass

class Void(General):
    """Объект-пустышка для Void/null-паттерна."""
    def __repr__(self):
        return "Void"
VoidInstance = Void()

# ======= Реализация объекта-произвольного типа Integer =======

class Integer(Any):
    def __init__(self, value):
        self.value = value
    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        return VoidInstance
    def __repr__(self):
        return f"Integer({self.value})"

# ======= Класс Vector<T> =======

class Vector(General):
    def __init__(self, elements):
        # elements — список объектов, наследующихся от General
        self.elements = list(elements)
    def __add__(self, other):
        if not isinstance(other, Vector):
            return VoidInstance
        if len(self.elements) != len(other.elements):
            return VoidInstance
        result = []
        for x, y in zip(self.elements, other.elements):
            try:
                s = x + y
            except Exception:
                return VoidInstance
            if isinstance(s, Void):
                return VoidInstance
            result.append(s)
        return Vector(result)
    def __repr__(self):
        return f"Vector({self.elements})"

# ======= Демонстрация работы =======

if __name__ == "__main__":
    print("=== Vector<Integer> ===")
    a = Vector([Integer(1), Integer(2)])
    b = Vector([Integer(10), Integer(20)])
    print("a:", a)
    print("b:", b)
    print("a + b :", a + b)

    print("\n=== Несовпадающие размеры ===")
    v1 = Vector([Integer(1), Integer(2)])
    v2 = Vector([Integer(10)])
    print("v1:", v1)
    print("v2:", v2)
    print("v1 + v2:", v1 + v2)

    print("\n=== Vector<Vector<Integer>> ===")
    va = Vector([a, b])      # Vector из Vector<Integer>
    vb = Vector([b, a])
    print("va:", va)
    print("vb:", vb)
    print("va + vb:", va + vb)

    print("\n=== Vector<Vector<Vector<Integer>>> ===")
    deep1 = Vector([va, vb])
    deep2 = Vector([vb, va])
    print("deep1:", deep1)
    print("deep2:", deep2)
    print("deep1 + deep2:", deep1 + deep2)

    print("\n=== Ошибка на уровне элементов ===")
    class Dummy(Any):
        def __repr__(self): return "Dummy"
    c = Vector([Integer(5), Dummy()])
    print("a:", a)
    print("c:", c)
    print("a + c:", a + c)
