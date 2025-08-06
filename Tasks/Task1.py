from abc import ABC, abstractmethod
from typing import List


# Абстрактный базовый класс для всех персонажей
class Character(ABC):
    """Базовый класс для всех персонажей в игре"""

    def __init__(self, name: str, health: int, mana: int):
        self.name = name
        self._health = health  # Инкапсуляция - приватный атрибут
        self._max_health = health
        self._mana = mana
        self._max_mana = mana
        self.inventory = Inventory()  # Композиция - персонаж содержит инвентарь

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = max(0, min(value, self._max_health))

    @abstractmethod
    def attack(self) -> int:
        """Полиморфизм - каждый класс реализует атаку по-своему"""
        pass

    def take_damage(self, damage: int):
        self.health -= damage
        print(f"{self.name} получил {damage} урона. Здоровье: {self.health}")


# НАСЛЕДОВАНИЕ - классы персонажей наследуются от Character
class Warrior(Character):
    """Воин - наследует от Character"""

    def __init__(self, name: str):
        super().__init__(name, health=120, mana=30)
        self.rage = 0

    def attack(self) -> int:
        """Реализация атаки воина"""
        damage = 25 + self.rage
        self.rage = min(self.rage + 5, 50)  # Накапливаем ярость
        print(f"{self.name} наносит мощный удар на {damage} урона!")
        return damage


class Mage(Character):
    """Маг - наследует от Character"""

    def __init__(self, name: str):
        super().__init__(name, health=80, mana=150)

    def attack(self) -> int:
        """Реализация атаки мага"""
        if self._mana >= 20:
            self._mana -= 20
            damage = 35
            print(f"{self.name} кастует огненный шар на {damage} урона!")
            return damage
        else:
            damage = 10
            print(f"{self.name} бьет посохом на {damage} урона (не хватает маны)")
            return damage


class Rogue(Character):
    """Разбойник - наследует от Character"""

    def __init__(self, name: str):
        super().__init__(name, health=90, mana=60)
        self.stealth = False

    def attack(self) -> int:
        """Реализация атаки разбойника"""
        base_damage = 20
        if self.stealth:
            damage = base_damage * 2  # Критический удар из скрытности
            self.stealth = False
            print(f"{self.name} наносит критический удар из тени на {damage} урона!")
        else:
            damage = base_damage
            print(f"{self.name} быстро атакует кинжалом на {damage} урона!")
        return damage

    def enter_stealth(self):
        """Уникальная способность разбойника"""
        self.stealth = True
        print(f"{self.name} скрывается в тенях...")


# КОМПОЗИЦИЯ - классы содержат другие объекты как компоненты
class Weapon:
    """Класс оружия"""

    def __init__(self, name: str, damage: int, weapon_type: str):
        self.name = name
        self.damage = damage
        self.weapon_type = weapon_type


class Inventory:
    """Инвентарь - содержится в персонаже (композиция)"""

    def __init__(self):
        self.items: List[Weapon] = []
        self.equipped_weapon: Weapon = None

    def add_item(self, item: Weapon):
        self.items.append(item)
        print(f"Получен предмет: {item.name}")

    def equip_weapon(self, weapon: Weapon):
        if weapon in self.items:
            self.equipped_weapon = weapon
            print(f"Экипировано оружие: {weapon.name}")


# Демонстрация ПОЛИМОРФИЗМА
def battle_simulation(attacker: Character, defender: Character):
    """
    Полиморфизм - функция работает с любым типом персонажа,
    вызывая их специфические реализации метода attack()
    """
    print(f"\n=== Бой между {attacker.name} и {defender.name} ===")

    # Каждый персонаж атакует по-своему (полиморфизм)
    damage = attacker.attack()
    defender.take_damage(damage)

    if defender.health > 0:
        damage = defender.attack()
        attacker.take_damage(damage)


# Пример использования
if __name__ == "__main__":
    # Создаем персонажей разных классов
    warrior = Warrior("Торин")
    mage = Mage("Гэндальф")
    rogue = Rogue("Арагорн")

    # Композиция - добавляем оружие в инвентарь
    sword = Weapon("Меч драконоборца", 30, "меч")
    warrior.inventory.add_item(sword)
    warrior.inventory.equip_weapon(sword)

    # Полиморфизм - одна функция работает с разными типами персонажей
    battle_simulation(warrior, mage)

    # Уникальные способности классов
    rogue.enter_stealth()
    battle_simulation(rogue, warrior)

    # Демонстрация полиморфизма - список разных персонажей
    party = [warrior, mage, rogue]
    print(f"\n=== Атака всей группы ===")
    for character in party:
        character.attack()  # Каждый атакует по-своему
