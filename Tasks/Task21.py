"""
Задание 21: Наследование реализации и льготное наследование

Примеры демонстрируют:
1. Наследование реализации - когда класс-потомок наследует полностью реализованный класс-предок
2. Льготное наследование - когда класс-предок содержит стандартный набор компонентов для удобства
"""

# ============================================================================
# 1. НАСЛЕДОВАНИЕ РЕАЛИЗАЦИИ (Implementation Inheritance)
# ============================================================================

class BaseCollection:
    """
    Базовый класс с полной реализацией коллекции.
    Демонстрирует наследование реализации - потомки наследуют
    готовую реализацию и добавляют свою уникальную функциональность.
    """
    
    def __init__(self):
        self._items = []
        self._size = 0
    
    def add(self, item):
        """Добавление элемента"""
        self._items.append(item)
        self._size += 1
    
    def remove(self, item):
        """Удаление элемента"""
        if item in self._items:
            self._items.remove(item)
            self._size -= 1
            return True
        return False
    
    def size(self):
        """Получение размера коллекции"""
        return self._size
    
    def is_empty(self):
        """Проверка на пустоту"""
        return self._size == 0
    
    def clear(self):
        """Очистка коллекции"""
        self._items.clear()
        self._size = 0


class UniqueCollection(BaseCollection):
    """
    Наследование реализации: наследует полную реализацию BaseCollection
    и добавляет уникальную функциональность - хранение только уникальных элементов.
    """
    
    def add(self, item):
        """Переопределение метода с добавлением уникальности"""
        if item not in self._items:
            super().add(item)
    
    def get_unique_count(self):
        """Уникальная функциональность потомка"""
        return len(set(self._items))


class SortedCollection(BaseCollection):
    """
    Наследование реализации: наследует полную реализацию BaseCollection
    и добавляет сортировку элементов.
    """
    
    def add(self, item):
        """Переопределение метода с добавлением сортировки"""
        super().add(item)
        self._items.sort()
    
    def get_sorted_items(self):
        """Уникальная функциональность потомка"""
        return self._items.copy()


# ============================================================================
# 2. ЛЬГОТНОЕ НАСЛЕДОВАНИЕ (Facility Inheritance)
# ============================================================================

class BaseException:
    """
    Базовый класс исключений с набором стандартных компонентов.
    Демонстрирует льготное наследование - содержит стандартный набор
    механизмов для удобства использования потомками.
    """
    
    def __init__(self, message="", error_code=None):
        self.message = message
        self.error_code = error_code
        self.timestamp = self._get_current_timestamp()
        self.context = {}
    
    def _get_current_timestamp(self):
        """Внутренний метод для получения времени"""
        import datetime
        return datetime.datetime.now()
    
    def add_context(self, key, value):
        """Добавление контекстной информации"""
        self.context[key] = value
    
    def get_full_message(self):
        """Формирование полного сообщения об ошибке"""
        result = f"Ошибка: {self.message}"
        if self.error_code:
            result += f" (код: {self.error_code})"
        if self.context:
            result += f" | Контекст: {self.context}"
        return result
    
    def __str__(self):
        return self.get_full_message()
    
    def __repr__(self):
        return f"{self.__class__.__name__}(message='{self.message}', error_code={self.error_code})"


class ValidationError(BaseException):
    """
    Льготное наследование: наследует стандартный набор компонентов
    для обработки ошибок валидации.
    """
    
    def __init__(self, field_name, invalid_value, expected_format=None):
        message = f"Ошибка валидации поля '{field_name}' со значением '{invalid_value}'"
        if expected_format:
            message += f". Ожидаемый формат: {expected_format}"
        
        super().__init__(message, error_code="VALIDATION_ERROR")
        self.field_name = field_name
        self.invalid_value = invalid_value
        self.expected_format = expected_format


class DatabaseError(BaseException):
    """
    Льготное наследование: наследует стандартный набор компонентов
    для обработки ошибок базы данных.
    """
    
    def __init__(self, operation, table_name, details=None):
        message = f"Ошибка базы данных при операции '{operation}' с таблицей '{table_name}'"
        if details:
            message += f": {details}"
        
        super().__init__(message, error_code="DATABASE_ERROR")
        self.operation = operation
        self.table_name = table_name
        self.details = details


class NetworkError(BaseException):
    """
    Льготное наследование: наследует стандартный набор компонентов
    для обработки сетевых ошибок.
    """
    
    def __init__(self, url, status_code=None, response_text=None):
        message = f"Сетевая ошибка при обращении к '{url}'"
        if status_code:
            message += f" (статус: {status_code})"
        
        super().__init__(message, error_code="NETWORK_ERROR")
        self.url = url
        self.status_code = status_code
        self.response_text = response_text


# ============================================================================
# ДЕМОНСТРАЦИЯ РАБОТЫ
# ============================================================================

def demonstrate_implementation_inheritance():
    """Демонстрация наследования реализации"""
    print("=== НАСЛЕДОВАНИЕ РЕАЛИЗАЦИИ ===")
    
    # Базовый класс
    base = BaseCollection()
    base.add(1)
    base.add(2)
    base.add(3)
    print(f"Базовая коллекция: размер = {base.size()}")
    
    # Наследование реализации - уникальная коллекция
    unique = UniqueCollection()
    unique.add(1)
    unique.add(1)  # Дубликат не добавится
    unique.add(2)
    unique.add(2)  # Дубликат не добавится
    print(f"Уникальная коллекция: размер = {unique.size()}, уникальных = {unique.get_unique_count()}")
    
    # Наследование реализации - сортированная коллекция
    sorted_coll = SortedCollection()
    sorted_coll.add(3)
    sorted_coll.add(1)
    sorted_coll.add(2)
    print(f"Сортированная коллекция: {sorted_coll.get_sorted_items()}")


def demonstrate_facility_inheritance():
    """Демонстрация льготного наследования"""
    print("\n=== ЛЬГОТНОЕ НАСЛЕДОВАНИЕ ===")
    
    # Создание различных типов исключений
    validation_error = ValidationError("email", "invalid-email", "user@domain.com")
    validation_error.add_context("form_id", "registration")
    
    db_error = DatabaseError("INSERT", "users", "Duplicate entry for key 'email'")
    db_error.add_context("user_id", 12345)
    
    network_error = NetworkError("https://api.example.com/users", 404, "Not Found")
    network_error.add_context("retry_count", 3)
    
    # Вывод информации об исключениях
    print("Ошибка валидации:")
    print(f"  {validation_error}")
    print(f"  Время: {validation_error.timestamp}")
    
    print("\nОшибка базы данных:")
    print(f"  {db_error}")
    print(f"  Контекст: {db_error.context}")
    
    print("\nСетевая ошибка:")
    print(f"  {network_error}")
    print(f"  URL: {network_error.url}, Статус: {network_error.status_code}")


if __name__ == "__main__":
    demonstrate_implementation_inheritance()
    demonstrate_facility_inheritance() 