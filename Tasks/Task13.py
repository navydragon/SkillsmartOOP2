"""
Python поддерживает реализацию всех четырех вариантов скрытия методов при наследовании благодаря гибкой 
системе соглашений об именах и динамической природе языка. 
Вариант 1 (Публичный → Публичный) реализуется естественным образом через стандартное переопределение методов 
без префиксов. 
Вариант 2 (Публичный → Скрытый) достигается через добавление префикса _ к имени метода или генерацию 
исключений NotImplementedError в переопределенном методе, что делает его фактически недоступным для 
использования. 
Вариант 3 (Скрытый → Публичный) реализуется простым удалением префикса _ из имени метода в дочернем классе, 
что делает ранее скрытый метод частью публичного API. 

Вариант 4 (Скрытый → Скрытый) работает по умолчанию 
- методы с префиксом _ остаются скрытыми во всей иерархии наследования, но могут быть переопределены в 
дочерних классах для специфической логики. 

Важно отметить, что Python использует соглашения об 
именах (convention-based hiding) rather than strict access control, поэтому все варианты основаны на дисциплине 
программиста и статических анализаторах кода, а не на жестких ограничениях времени выполнения.
"""
from abc import ABC, abstractmethod

class Vehicle(ABC):
    """
    Базовый абстрактный класс для всех транспортных средств.
    Содержит общие методы и определяет интерфейс.
    """
    
    def __init__(self, brand: str, model: str, year: int):
        self._brand = brand
        self._model = model
        self._year = year
        self._is_running = False
    
    # Публичные методы - основной интерфейс
    def start(self):
        """Публичный метод запуска транспортного средства"""
        if not self._is_running:
            self._perform_startup_sequence()
            self._is_running = True
            return f"{self._brand} {self._model} запущен"
        return "Уже запущен"
    
    def stop(self):
        """Публичный метод остановки"""
        if self._is_running:
            self._perform_shutdown_sequence()
            self._is_running = False
            return f"{self._brand} {self._model} остановлен"
        return "Уже остановлен"
    
    def get_info(self):
        """Публичный метод получения информации"""
        return f"{self._brand} {self._model} ({self._year})"
    
    def honk(self):
        """Публичный метод подачи сигнала"""
        return "Общий сигнал"
    
    # Защищенные методы - для наследников
    def _perform_startup_sequence(self):
        """Скрытый метод последовательности запуска"""
        return "Выполняю базовую последовательность запуска"
    
    def _perform_shutdown_sequence(self):
        """Скрытый метод последовательности остановки"""
        return "Выполняю базовую последовательность остановки"
    
    def _check_fuel_level(self):
        """Скрытый метод проверки уровня топлива"""
        return "Проверяю уровень топлива"
    
    def _diagnostic_check(self):
        """Скрытый метод диагностики"""
        return "Выполняю диагностику"
    
    # Абстрактные методы
    @abstractmethod
    def move(self):
        """Абстрактный метод движения"""
        pass


class Car(Vehicle):
    """
    Автомобиль - демонстрация варианта 1: Публичный → Публичный
    """
    
    def __init__(self, brand: str, model: str, year: int, fuel_type: str):
        super().__init__(brand, model, year)
        self._fuel_type = fuel_type
    
    # Вариант 1: Публичный → Публичный
    def start(self):
        """Публичный метод остается публичным, но переопределен"""
        result = super().start()
        if "запущен" in result:
            return f"Автомобиль {result}. Двигатель работает на {self._fuel_type}"
        return result
    
    def stop(self):
        """Публичный метод остается публичным"""
        result = super().stop()
        if "остановлен" in result:
            return f"Автомобиль {result}. Двигатель заглушен"
        return result
    
    def honk(self):
        """Публичный метод остается публичным с новой реализацией"""
        return "Би-би! (автомобильный гудок)"
    
    def get_info(self):
        """Публичный метод остается публичным, расширен"""
        base_info = super().get_info()
        return f"{base_info}, топливо: {self._fuel_type}"
    
    def move(self):
        """Реализация абстрактного метода - публичный"""
        return "Еду по дороге"
    
    # Новые публичные методы
    def open_doors(self):
        """Новый публичный метод"""
        return "Двери открыты"
    
    def close_doors(self):
        """Новый публичный метод"""
        return "Двери закрыты"





class Bicycle(Vehicle):
    """
    Велосипед - демонстрация варианта 2: Публичный → Скрытый
    """
    
    def __init__(self, brand: str, model: str, year: int, gear_count: int):
        super().__init__(brand, model, year)
        self._gear_count = gear_count
    
    # Вариант 2: Публичный → Скрытый
    def start(self):
        """Публичный метод скрыт - велосипед не запускается"""
        raise NotImplementedError("Велосипед не требует запуска двигателя")
    
    def stop(self):
        """Публичный метод скрыт - велосипед не останавливается как мотор"""
        raise NotImplementedError("Велосипед не имеет двигателя для остановки")
    
    def _hidden_start(self):
        """Оригинальная логика запуска теперь скрыта"""
        return "Велосипедист готов к поездке"
    
    def _hidden_stop(self):
        """Оригинальная логика остановки теперь скрыта"""
        return "Велосипедист остановился"
    
    # Публичные методы остаются публичными
    def honk(self):
        """Публичный метод остается публичным"""
        return "Дзинь-дзинь! (велосипедный звонок)"
    
    def get_info(self):
        """Публичный метод остается публичным"""
        base_info = super().get_info()
        return f"{base_info}, передач: {self._gear_count}"
    
    def move(self):
        """Реализация абстрактного метода"""
        return "Еду на велосипеде"
    
    # Новые публичные методы вместо скрытых
    def prepare_to_ride(self):
        """Новый публичный метод вместо start()"""
        return self._hidden_start()
    
    def finish_ride(self):
        """Новый публичный метод вместо stop()"""
        return self._hidden_stop()
    
    def change_gear(self, gear: int):
        """Специфичный для велосипеда метод"""
        if 1 <= gear <= self._gear_count:
            return f"Переключена {gear} передача"
        return "Недопустимая передача"


class DiagnosticCar(Car):
    """
    Автомобиль с диагностическими функциями - демонстрация варианта 3: Скрытый → Публичный
    """
    
    def __init__(self, brand: str, model: str, year: int, fuel_type: str):
        super().__init__(brand, model, year, fuel_type)
        self._diagnostic_mode = False
    
    # Вариант 3: Скрытый → Публичный
    def diagnostic_check(self):
        """Скрытый метод родителя стал публичным"""
        self._diagnostic_mode = True
        result = self._diagnostic_check()
        diagnostic_info = self._get_detailed_diagnostics()
        return f"{result}. {diagnostic_info}"
    
    def check_fuel_level(self):
        """Скрытый метод родителя стал публичным"""
        fuel_info = self._check_fuel_level()
        return f"{fuel_info}. Текущий уровень: 75%"
    
    def perform_startup_sequence(self):
        """Скрытый метод родителя стал публичным для диагностики"""
        if self._diagnostic_mode:
            return f"Диагностический режим: {self._perform_startup_sequence()}"
        return "Диагностический режим не активен"
    
    def perform_shutdown_sequence(self):
        """Скрытый метод родителя стал публичным для диагностики"""
        if self._diagnostic_mode:
            return f"Диагностический режим: {self._perform_shutdown_sequence()}"
        return "Диагностический режим не активен"
    
    # Новые скрытые методы
    def _get_detailed_diagnostics(self):
        """Новый скрытый метод"""
        return "Подробная диагностика: все системы в норме"
    
    def _enable_diagnostic_mode(self):
        """Новый скрытый метод"""
        self._diagnostic_mode = True
    
    def _disable_diagnostic_mode(self):
        """Новый скрытый метод"""
        self._diagnostic_mode = False
    
    # Публичные методы для управления диагностикой
    def enable_diagnostics(self):
        """Публичный метод активации диагностики"""
        self._enable_diagnostic_mode()
        return "Диагностический режим активирован"
    
    def disable_diagnostics(self):
        """Публичный метод деактивации диагностики"""
        self._disable_diagnostic_mode()
        return "Диагностический режим деактивирован"


class Motorcycle(Vehicle):
    """
    Мотоцикл - демонстрация варианта 4: Скрытый → Скрытый
    """
    
    def __init__(self, brand: str, model: str, year: int, engine_size: int):
        super().__init__(brand, model, year)
        self._engine_size = engine_size
        self._kickstand_down = True
    
    # Публичные методы
    def start(self):
        """Публичный метод с проверкой подножки"""
        if self._kickstand_down:
            return "Нельзя запустить мотоцикл с опущенной подножкой"
        return super().start()
    
    def honk(self):
        """Публичный метод остается публичным"""
        return "Врум-врум! (мотоциклетный сигнал)"
    
    def get_info(self):
        """Публичный метод остается публичным"""
        base_info = super().get_info()
        return f"{base_info}, объем двигателя: {self._engine_size}cc"
    
    def move(self):
        """Реализация абстрактного метода"""
        return "Еду на мотоцикле"
    
    # Вариант 4: Скрытый → Скрытый (переопределение скрытых методов)
    def _perform_startup_sequence(self):
        """Скрытый метод остается скрытым, но переопределен"""
        base_startup = super()._perform_startup_sequence()
        return f"{base_startup}. Прогреваю мотоциклетный двигатель {self._engine_size}cc"
    
    def _perform_shutdown_sequence(self):
        """Скрытый метод остается скрытым, но переопределен"""
        base_shutdown = super()._perform_shutdown_sequence()
        return f"{base_shutdown}. Выключаю мотоциклетный двигатель"
    
    def _check_fuel_level(self):
        """Скрытый метод остается скрытым, но переопределен"""
        base_check = super()._check_fuel_level()
        return f"{base_check} в баке мотоцикла"
    
    def _diagnostic_check(self):
        """Скрытый метод остается скрытым, но переопределен"""
        base_diagnostic = super()._diagnostic_check()
        return f"{base_diagnostic} мотоцикла"
    
    # Новые скрытые методы
    def _check_kickstand(self):
        """Новый скрытый метод проверки подножки"""
        return "Подножка поднята" if not self._kickstand_down else "Подножка опущена"
    
    def _warm_up_engine(self):
        """Новый скрытый метод прогрева двигателя"""
        return f"Прогреваю двигатель {self._engine_size}cc"
    
    def _check_tire_pressure(self):
        """Новый скрытый метод проверки давления в шинах"""
        return "Проверяю давление в шинах мотоцикла"
    
    # Публичные методы для управления подножкой
    def raise_kickstand(self):
        """Публичный метод поднятия подножки"""
        self._kickstand_down = False
        return "Подножка поднята"
    
    def lower_kickstand(self):
        """Публичный метод опускания подножки"""
        self._kickstand_down = True
        return "Подножка опущена"


def demonstrate_visibility_variants():
    """Демонстрация всех четырех вариантов скрытия методов"""
    
    print("=== Демонстрация вариантов скрытия методов в области Vehicle ===\n")
    
    # Создание объектов
    car = Car("Toyota", "Camry", 2023, "бензин")
    bicycle = Bicycle("Trek", "Mountain", 2023, 21)
    diagnostic_car = DiagnosticCar("BMW", "X5", 2023, "дизель")
    motorcycle = Motorcycle("Harley-Davidson", "Sportster", 2023, 883)
    
    # Вариант 1: Публичный → Публичный
    print("1. ВАРИАНТ 1: Публичный → Публичный")
    print("   Методы остаются публичными, но могут быть переопределены")
    print(f"   Car start: {car.start()}")
    print(f"   Car honk: {car.honk()}")
    print(f"   Car info: {car.get_info()}")
    print(f"   Car move: {car.move()}")
    
    # Вариант 2: Публичный → Скрытый
    print("\n2. ВАРИАНТ 2: Публичный → Скрытый")
    print("   Публичные методы родителя скрываются в потомке")
    print(f"   Bicycle honk: {bicycle.honk()}")  # Остается публичным
    print(f"   Bicycle move: {bicycle.move()}")
    
    try:
        bicycle.start()  # Скрыт
    except NotImplementedError as e:
        print(f"   Bicycle start (скрыт): {e}")
    
    print(f"   Bicycle prepare_to_ride: {bicycle.prepare_to_ride()}")  # Новый публичный
    
    # Вариант 3: Скрытый → Публичный
    print("\n3. ВАРИАНТ 3: Скрытый → Публичный")
    print("   Скрытые методы родителя становятся публичными")
    print(f"   DiagnosticCar enable_diagnostics: {diagnostic_car.enable_diagnostics()}")
    print(f"   DiagnosticCar diagnostic_check: {diagnostic_car.diagnostic_check()}")
    print(f"   DiagnosticCar check_fuel_level: {diagnostic_car.check_fuel_level()}")
    print(f"   DiagnosticCar startup_sequence: {diagnostic_car.perform_startup_sequence()}")
    
    # Вариант 4: Скрытый → Скрытый
    print("\n4. ВАРИАНТ 4: Скрытый → Скрытый")
    print("   Скрытые методы остаются скрытыми, но могут быть переопределены")
    print(f"   Motorcycle raise_kickstand: {motorcycle.raise_kickstand()}")
    print(f"   Motorcycle start: {motorcycle.start()}")
    
    # Демонстрация работы скрытых методов (не рекомендуется в production)
    print("\n   Технический доступ к скрытым методам (только для демонстрации):")
    print(f"   Car _check_fuel_level: {car._check_fuel_level()}")
    print(f"   Motorcycle _check_fuel_level: {motorcycle._check_fuel_level()}")
    print(f"   Motorcycle _check_kickstand: {motorcycle._check_kickstand()}")

if __name__ == "__main__":
    demonstrate_visibility_variants()
