class BattleSystem:
    def __init__(self, trainer1, trainer2):
        self.trainer1 = trainer1
        self.trainer2 = trainer2
        self.turn_count = 0

    def run_turn(self, action1, action2) -> None:
        self.turn_count += 1
        pairs = [(self.trainer1, action1), (self.trainer2, action2)]

        # PHA 1 — switch luôn xử lý trước, bất kể speed
        for trainer, action in pairs:
            if action["type"] == "switch":
                success = trainer.switch_to(action["index"])
                if not success:
                    print(f"{trainer.name} switch thất bại!")

        # PHA 2 — chỉ những ai chọn move mới cần xác định thứ tự đánh
        move_pairs = [(t, a["move"]) for t, a in pairs if a["type"] == "move"]

        def sort_key(pair):
            trainer, move = pair
            pokemon = trainer.get_active()
            # số càng nhỏ càng đánh trước -> đảo dấu để ưu tiên cao/speed cao lên đầu
            return (-move.priority, -pokemon.get_effective_stat("speed"))

        move_pairs.sort(key=sort_key)

        # PHA 3 — thực thi move theo đúng thứ tự vừa sắp
        for trainer, move in move_pairs:
            user = trainer.get_active()
            opponent = self.trainer2 if trainer is self.trainer1 else self.trainer1
            target = opponent.get_active()

            if user.is_fainted():
                continue  # đã bị hạ gục bởi đòn đánh trước đó trong CÙNG turn này

            if user.status_condition is not None:
                can_act = user.status_condition.on_turn_start(user)
                if not can_act:
                    continue

            move.execute(user, target)

        # PHA 4 — cuối turn: áp on_turn_end cho cả 2 bên
        for trainer in (self.trainer1, self.trainer2):
            pokemon = trainer.get_active()
            if not pokemon.is_fainted() and pokemon.status_condition is not None:
                pokemon.status_condition.on_turn_end(pokemon)

    def is_battle_over(self) -> bool:
        return not self.trainer1.has_available_pokemon() or not self.trainer2.has_available_pokemon()

    def get_winner(self):
        if not self.trainer1.has_available_pokemon():
            return self.trainer2
        if not self.trainer2.has_available_pokemon():
            return self.trainer1
        return None