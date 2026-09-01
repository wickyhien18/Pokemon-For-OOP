import random
from Effect import Effect

class Move:
    def __init__(self, name: str, accuracy: int, priority: int, effects: list[Effect]):
        self.name = name
        self.accuracy = accuracy
        self.priority = priority
        self.effects = effects

    def execute(self, user, target):
        if random.random() * 100 > self.accuracy:
            print(f"{user.name} use {self.name} but missed")
            return
        for effect in self.effects:
            effect.apply(user, target)