class Pokemon:
    def __init__(self, name, types: list[str], level, base_hp, base_atk, 
                 base_def, base_sp_atk, base_sp_def, base_speed, moves):
        self.name = name
        self.types = types
        self.level = level
        self.moves = moves

        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_sp_atk = base_sp_atk
        self.base_sp_def = base_sp_def
        self.base_speed = base_speed

        self.max_hp = self._calc_hp_stat()
        self.atk = self._calc_stat(base_atk)
        self.def_ = self._calc_stat(base_def)
        self.sp_atk = self._calc_stat(base_sp_atk)
        self.sp_def = self._calc_stat(base_sp_def)
        self.speed = self._calc_stat(base_speed)

        self.current_hp = self.max_hp

        self.status_condition = None
        self.stat_stages = {"atk": 0, "def": 0, "sp_atk" : 0, "sp_def": 0, "speed": 0, "accuracy": 0}

    def _calc_hp_stat(self) -> int:
        return int(self.base_hp * (1 + self.level / 50)) + self.level

    def _calc_stat(self, base: int) -> int:
        return int(base * (1 + self.level / 100)) + 5

    def take_damage(self, dmg: int) -> None:
        self.current_hp = max(0, self.current_hp - dmg)

    def is_fainted(self) -> bool:
        return self.current_hp <= 0

    def get_stat_multiplier(self, stat_name: str) -> float:
        stage = self.stat_stages[stat_name]
        return 1 + stage * 0.25

    def get_effective_stat(self, stat_name: str) -> int:
        attr_name = stat_name + "_" if stat_name == "def" else stat_name
        raw_value = getattr(self, attr_name)
        return int(raw_value * self.get_stat_multiplier(stat_name))

    def apply_status(self, status) -> None:
        self.status_condition = status
        status.on_apply(self)

    def __repr__(self) -> str:
        return f"Pokemon({self.name}, HP {self.current_hp}/{self.max_hp})"