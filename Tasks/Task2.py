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


class Warrior(Character):
    """Воин - демонстрирует РАСШИРЕНИЕ и СПЕЦИАЛИЗАЦИЮ"""

    def __init__(self, name: str):
        super().__init__(name, health=120, mana=30)
        # РАСШИРЕНИЕ: добавляем новый атрибут, которого нет у родителя
        self.rage = 0

    # СПЕЦИАЛИЗАЦИЯ: переопределяем абстрактный метод родителя
    def attack(self) -> int:
        """СПЕЦИАЛИЗАЦИЯ: конкретная реализация атаки воина"""
        damage = 25 + self.rage
        self.rage = min(self.rage + 5, 50)  # Накапливаем ярость
        print(f"{self.name} наносит мощный удар на {damage} урона!")
        return damage

    # РАСШИРЕНИЕ: добавляем новый метод, которого нет у родителя
    def berserker_rage(self):
        """РАСШИРЕНИЕ: новая уникальная способность воина"""
        self.rage = 50
        print(f"{self.name} впадает в ярость берсерка! Ярость максимальна!")

    # СПЕЦИАЛИЗАЦИЯ: переопределяем метод родителя с дополнительной логикой
    def take_damage(self, damage: int):
        """СПЕЦИАЛИЗАЦИЯ: переопределяем получение урона с накоплением ярости"""
        super().take_damage(damage)  # Вызываем базовую логику
        # Добавляем специфическую логику воина
        self.rage = min(self.rage + 2, 50)
        print(f"Ярость воина увеличилась до {self.rage}")


class Mage(Character):
    """Маг - демонстрирует РАСШИРЕНИЕ и СПЕЦИАЛИЗАЦИЮ"""

    def __init__(self, name: str):
        super().__init__(name, health=80, mana=150)
        # РАСШИРЕНИЕ: добавляем новые атрибуты
        self.spell_power = 10
        self.mana_regeneration = 5

    # СПЕЦИАЛИЗАЦИЯ: переопределяем абстрактный метод родителя
    def attack(self) -> int:
        """СПЕЦИАЛИЗАЦИЯ: магическая атака с расходом маны"""
        if self._mana >= 20:
            self._mana -= 20
            damage = 35 + self.spell_power
            print(f"{self.name} кастует огненный шар на {damage} урона!")
            return damage
        else:
            damage = 10
            print(f"{self.name} бьет посохом на {damage} урона (не хватает маны)")
            return damage

    # РАСШИРЕНИЕ: добавляем новые методы
    def meditate(self):
        """РАСШИРЕНИЕ: новая способность восстановления маны"""
        restored = min(self.mana_regeneration * 6, self._max_mana - self._mana)
        self._mana += restored
        print(f"{self.name} медитирует и восстанавливает {restored} маны")

    def cast_fireball(self, target: "Character"):
        """РАСШИРЕНИЕ: новое заклинание"""
        if self._mana >= 30:
            self._mana -= 30
            damage = 45 + self.spell_power
            print(f"{self.name} кастует мощный огненный шар!")
            target.take_damage(damage)
        else:
            print(f"{self.name} недостаточно маны для заклинания")


class Rogue(Character):
    """Разбойник - демонстрирует РАСШИРЕНИЕ и СПЕЦИАЛИЗАЦИЮ"""

    def __init__(self, name: str):
        super().__init__(name, health=90, mana=60)
        # РАСШИРЕНИЕ: добавляем новые атрибуты
        self.stealth = False
        self.critical_chance = 0.3
        self.agility = 15

    # СПЕЦИАЛИЗАЦИЯ: переопределяем абстрактный метод родителя
    def attack(self) -> int:
        """СПЕЦИАЛИЗАЦИЯ: атака с критическим уроном из скрытности"""
        base_damage = 20
        if self.stealth:
            damage = base_damage * 2  # Критический удар из скрытности
            self.stealth = False
            print(f"{self.name} наносит критический удар из тени на {damage} урона!")
        else:
            damage = base_damage
            print(f"{self.name} быстро атакует кинжалом на {damage} урона!")
        return damage

    # РАСШИРЕНИЕ: добавляем новые методы
    def enter_stealth(self):
        """РАСШИРЕНИЕ: уникальная способность скрытности"""
        self.stealth = True
        print(f"{self.name} скрывается в тенях...")

    def backstab(self, target: "Character"):
        """РАСШИРЕНИЕ: новая способность удара в спину"""
        if self.stealth:
            damage = 40 + self.agility
            print(f"{self.name} наносит удар в спину на {damage} урона!")
            target.take_damage(damage)
            self.stealth = False
        else:
            print(f"{self.name} должен быть в скрытности для удара в спину")

    def dodge_roll(self):
        """РАСШИРЕНИЕ: новая способность уклонения"""
        print(f"{self.name} делает кувырок, уклоняясь от атак!")
        return True  # В реальной игре это могло бы влиять на следующую атаку


# РАСШИРЕНИЕ базового класса - Paladin расширяет Character
class Paladin(Character):
    """Паладин - демонстрирует РАСШИРЕНИЕ базового класса"""

    def __init__(self, name: str):
        super().__init__(name, health=110, mana=100)
        # РАСШИРЕНИЕ: добавляем множество новых атрибутов
        self.holy_power = 0
        self.armor = 12
        self.faith = 20
        self.can_heal = True

    # СПЕЦИАЛИЗАЦИЯ: реализуем абстрактный метод
    def attack(self) -> int:
        """СПЕЦИАЛИЗАЦИЯ: священная атака"""
        base_damage = 25
        holy_bonus = self.holy_power * 3
        damage = base_damage + holy_bonus
        print(f"{self.name} наносит священный удар на {damage} урона!")
        if self.holy_power > 0:
            self.holy_power -= 1
        return damage

    # СПЕЦИАЛИЗАЦИЯ: переопределяем получение урона с учетом брони
    def take_damage(self, damage: int):
        """СПЕЦИАЛИЗАЦИЯ: получение урона с учетом брони и накопления святой силы"""
        actual_damage = max(1, damage - self.armor)
        super().take_damage(actual_damage)
        # Накапливаем святую силу при получении урона
        self.holy_power = min(self.holy_power + 1, 5)
        print(f"Святая сила увеличилась до {self.holy_power}")

    # РАСШИРЕНИЕ: добавляем множество новых методов
    def heal_ally(self, target: Character):
        """РАСШИРЕНИЕ: новая способность лечения"""
        if self._mana >= 25 and self.can_heal:
            self._mana -= 25
            heal_amount = 30 + self.faith
            target.health += heal_amount
            print(f"{self.name} лечит {target.name} на {heal_amount} здоровья")

    def divine_shield(self):
        """РАСШИРЕНИЕ: новая защитная способность"""
        if self.holy_power >= 2:
            self.armor += 10
            self.holy_power -= 2
            print(f"{self.name} активирует божественный щит! Броня: {self.armor}")

    def consecrate(self):
        """РАСШИРЕНИЕ: новая область поражения"""
        if self._mana >= 40:
            self._mana -= 40
            damage = 20 + self.faith
            print(f"{self.name} освящает землю, нанося {damage} урона всем врагам!")
            return damage

    def prayer(self):
        """РАСШИРЕНИЕ: новая способность молитвы"""
        restored_mana = self.faith
        restored_health = self.faith // 2
        self._mana = min(self._mana + restored_mana, self._max_mana)
        self.health += restored_health
        print(
            f"{self.name} молится, восстанавливая {restored_mana} маны и {restored_health} здоровья"
        )


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
    print("=== ДЕМОНСТРАЦИЯ РАСШИРЕНИЯ И СПЕЦИАЛИЗАЦИИ ===\n")

    # Создаем персонажей разных классов
    warrior = Warrior("Торин")
    mage = Mage("Гэндальф")
    rogue = Rogue("Арагорн")
    paladin = Paladin("Артур")

    print("1. РАСШИРЕНИЕ - новые атрибуты и методы:")
    print(f"Воин добавил: rage={warrior.rage}, метод berserker_rage()")
    print(
        f"Маг добавил: spell_power={mage.spell_power}, методы meditate(), cast_fireball()"
    )
    print(
        f"Разбойник добавил: stealth={rogue.stealth}, agility={rogue.agility}, методы backstab(), dodge_roll()"
    )
    print(
        f"Паладин добавил: holy_power={paladin.holy_power}, armor={paladin.armor}, faith={paladin.faith}"
    )

    print(f"\n2. СПЕЦИАЛИЗАЦИЯ - переопределение методов:")
    print("Каждый класс по-своему реализует attack() и некоторые take_damage()")

    # Демонстрация расширенных способностей
    print(f"\n3. Демонстрация РАСШИРЕНИЯ - новые способности:")
    warrior.berserker_rage()  # Новый метод воина
    mage.meditate()  # Новый метод мага
    rogue.enter_stealth()  # Новый метод разбойника
    paladin.prayer()  # Новый метод паладина

    print(f"\n4. Демонстрация СПЕЦИАЛИЗАЦИИ - переопределенные методы:")
    # Каждый ат
