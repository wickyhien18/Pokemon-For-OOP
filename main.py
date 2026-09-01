from Pokemon import Pokemon
from Effect import DamageEffect, InflictStatucEffect
from Move import Move
from Status import Burn
from Trainer import Trainer
from BattleSystem import BattleSystem


def make_team_ash():
    ember = Move(
        "Ember", accuracy=100, priority=0,
        effects=[
            DamageEffect(power=40, category="special"),
            InflictStatucEffect(Burn, chance=0.3),
        ],
    )
    charmander = Pokemon(
        "Charmander", ["Fire"], level=20,
        base_hp=39, base_atk=52, base_def=43,
        base_sp_atk=60, base_sp_def=50, base_speed=65,
        moves=[ember],
    )

    tackle = Move("Tackle", accuracy=100, priority=0,
                   effects=[DamageEffect(power=35, category="physical")])
    pidgey = Pokemon(
        "Pidgey", ["Normal", "Flying"], level=18,
        base_hp=40, base_atk=45, base_def=40,
        base_sp_atk=35, base_sp_def=35, base_speed=56,
        moves=[tackle],
    )
    return Trainer("Ash", [charmander, pidgey]), ember, tackle


def make_team_misty():
    tackle = Move("Tackle", accuracy=100, priority=0,
                   effects=[DamageEffect(power=35, category="physical")])
    squirtle = Pokemon(
        "Squirtle", ["Water"], level=20,
        base_hp=44, base_atk=48, base_def=65,
        base_sp_atk=50, base_sp_def=64, base_speed=43,
        moves=[tackle],
    )

    watergun = Move("Water Gun", accuracy=100, priority=0,
                     effects=[DamageEffect(power=40, category="special")])
    staryu = Pokemon(
        "Staryu", ["Water"], level=19,
        base_hp=30, base_atk=45, base_def=55,
        base_sp_atk=70, base_sp_def=55, base_speed=85,
        moves=[watergun],
    )
    return Trainer("Misty", [squirtle, staryu]), tackle, watergun


def print_status(trainer: Trainer) -> None:
    p = trainer.get_active()
    status = p.status_condition.__class__.__name__ if p.status_condition else "khỏe mạnh"
    print(f"  {trainer.name} -> {p.name}: {p.current_hp}/{p.max_hp} HP ({status})")


def main():
    ash, ember, ash_tackle = make_team_ash()
    misty, misty_tackle, watergun = make_team_misty()

    battle = BattleSystem(ash, misty)

    while not battle.is_battle_over():
        active_ash = ash.get_active()
        active_misty = misty.get_active()

        # Nếu Pokemon đang ra sân đã ngất, bắt buộc switch sang con còn sống
        # trước khi có thể dùng move trong turn tiếp theo.
        if active_ash.is_fainted():
            next_index = next(i for i, p in enumerate(ash.team) if not p.is_fainted())
            action_ash = {"type": "switch", "index": next_index}
        else:
            move = ember if active_ash.name == "Charmander" else ash_tackle
            action_ash = {"type": "move", "move": move}

        if active_misty.is_fainted():
            next_index = next(i for i, p in enumerate(misty.team) if not p.is_fainted())
            action_misty = {"type": "switch", "index": next_index}
        else:
            move = misty_tackle if active_misty.name == "Squirtle" else watergun
            action_misty = {"type": "move", "move": move}

        battle.run_turn(action_ash, action_misty)
        print_status(ash)
        print_status(misty)

    winner = battle.get_winner()
    print(f"\n>>> KẾT THÚC SAU {battle.turn_count} TURN — Người thắng: {winner.name} <<<")


if __name__ == "__main__":
    main()
