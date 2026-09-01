from abc import ABC, abstractmethod
import Pokemon
import random

class Effect(ABC):
    @abstractmethod
    def apply(self, user: "Pokemon", target: "Pokemon") -> None:
        ...

class DamageEffect(Effect):
    def __init__(self, power: int, category: str = "physical"):
        self.power = power
        self.category = category

    def apply(self, user, target) -> None:
        if self.category == "physical":
            atk_stat, def_stat = "atk", "def"
        else:
            atk_stat, def_stat = "sp_atk", "sp_def"

        atk_value = user.get_effective_stat(atk_stat)
        def_value = user.get_effective_stat(def_stat)

        damage = int(self.power * atk_value / def_value)

        target.take_damage(damage)
        print(f"{user.name} use {self.category} attack.\n {target.name} take {damage} damage")

class InflictStatucEffect(Effect):
    def __init__(self, status_cls, chance: float):
        self.status_cls = status_cls
        self.chance = chance
    
    def apply(self, user, target) -> None:
        if target.status_condition is not None:
            return
        if random.random < self.chance:
            target.apply_status(self.status_cls())

        print(f"{target.name} is afflicted with {self.status_cls.__name__}")
