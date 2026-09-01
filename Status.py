from abc import ABC
import random

class StatusCondition(ABC):
    def on_apply(self, pokemon) -> None:
        pass

    def on_turn_start(self, pokemon) -> bool:
        return True

    def on_turn_end(self, pokemon) -> None:
        pass

class Burn(StatusCondition):
    def on_turn_end(self, pokemon) -> None:
        dmg = pokemon.max_hp // 16
        pokemon.take_damage(dmg)
        print(f"{pokemon.name} is Burn, lost {dmg} HP")

class Poison(StatusCondition):
    def on_turn_end(self, pokemon) -> None:
        dmg = pokemon.max_hp // 8
        pokemon.take_damage(dmg)
        print(f"{pokemon.name} is Poison, lost {dmg} HP")

class Paralysis(StatusCondition):
    def on_apply(self, pokemon) -> None:
        pokemon.stat_stages["speed"] -= 1

    def on_turn_start(self, pokemon) -> bool:
        if random.random() < 0.25:
            print(f"{pokemon.name} is Paralysis, can't move")
            return False
        return True