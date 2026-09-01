from Pokemon import Pokemon

class Trainer:
    def __init__(self, name: str, team: list):
        self.name = name
        self.team = team
        self.active_index = 0

    def get_active(self):
        return self.team[self.active_index]

    def switch_to(self, index: int) -> bool:
        if index < 0 or index >= len(self.team):
            return False
        if self.team[index].is_fainted():
            return False

        self.active_index = index
        return True

    def has_available_pokemon(self) -> bool:
        return any(not p.is_fainted() for p in self.team) 
