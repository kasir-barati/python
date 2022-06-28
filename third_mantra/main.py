from .classes.person import Person
# from .types.magic import Magic
from .classes.spell import Spell
from .classes.style_me import style_me
from .classes.inventory import Item
from .enums.actions import Action


def main():
    magics = generate_dummy_magic_list()
    items = generate_dummy_item_list()
    player = Person("Kasir", 460, 65, 60, 34, magics, items)
    wizard = Person("Sun", 1200, 61, 67, 74, magics, items)

    initial_app_message = style_me("An enemy attacks!", is_failed=True, is_bold=True)
    print(initial_app_message)

    while True:
        player_generated_damage = act(player)
        if player_generated_damage:
            wizard.take_damage(player_generated_damage)

        wizard_generated_damage = act(wizard)
        if wizard_generated_damage:
            player.take_damage(wizard_generated_damage)

        print_player_and_enemy_status(player, wizard)
        print("\n\r------------------------\n\r")

        if is_battle_over([player, wizard]):
            break

    print_player_and_enemy_status(player, wizard)


def is_battle_over(fighters: list[Person]):
    for fighter in fighters:
        if fighter.get_hp() == 0:
            message = style_me(
                f"{fighter.name} is dead",
                is_failed=True,
                is_bold=True
            )
            print(message)

            return True;
    
    return False;


def act(person: Person) -> int|None:
    print(style_me("Press 0 to go back at any time", is_warned=True, is_bold=True, is_underlined=True))
    person.choose_action()
    chose_action_message = style_me(
        f"Make your move {person.name}: ", 
        is_bold=True,
        is_purple=True
    )
    chosen_action = input(chose_action_message)
    chosen_action = int(chosen_action)

    if chosen_action == Action.ATTACK.value:
        return person.generate_damage(action=Action.ATTACK)
    elif chosen_action == Action.MAGIC.value:
        person.choose_magic()
        chose_your_spell_message = style_me(
            "Chose your spell: ", 
            is_bold=True,
            is_purple=True
        )
        chosen_spell = input(chose_your_spell_message)
        chosen_spell = int(chosen_spell)

        if chosen_spell == 0:
            return act(person)
        
        maximum_valid_magic_index = len(person.magics)
        chosen_spell = chosen_spell - 1
        assert chosen_spell in range(0, maximum_valid_magic_index), "Chosen magic is invalid!"

        return person.generate_damage(
            action=Action.MAGIC, 
            magic_index=chosen_spell
        )
    elif chosen_action == Action.ITEM.value:
        person.choose_item()
    elif chosen_action == 0:
        return act(person)
    else:
        raise Exception("Your choice was out of range")
    

def print_player_and_enemy_status(player: Person, enemy: Person):
    current_wizard_hp = enemy.get_hp()
    current_wizard_mp = enemy.get_mp()
    current_player_hp = player.get_hp()
    current_player_mp = player.get_mp()
    wizard_hp_message = style_me(
        f"Wizard status: hp = {current_wizard_hp}, mp = {current_wizard_mp}",
        is_underlined=True,
        is_turquoise=True
    )
    player_hp_message = style_me(
        f"Your status: hp = {current_player_hp}, mp = {current_player_mp}",
        is_underlined=True,
        is_turquoise=True
    )
    
    print(wizard_hp_message + '. ' + player_hp_message)


def generate_dummy_magic_list() -> list[Spell]:
    fire = Spell("Fire", 10, 60, "black")
    thunder = Spell("Thunder", 10, 80, "black")
    blizzard = Spell("Blizzard", 10, 70, "black")
    heal = Spell("Heal", 5, 120, "white")
    cure = Spell("Cure", 15, 340, "white")

    return [
        fire,
        thunder,
        blizzard,
        heal,
        cure
    ]


def generate_dummy_item_list() -> list[Item]:
    potion = Item("Potion", "potion", "Heal 50 HP", 50)
    high_potion = Item("High Potion", "potion", "Heal 100 HP", 100)
    super_potion = Item("Super Potion", "potion", "Heal 500 HP", 500)
    elixer = Item("Elixer", "elixer", "Fully restores HP/MP of ones party member", 9999)
    mega_elixer = Item("Mega Elixer", "elixer", "Fully restores party's HP/MP", 9999)
    grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

    return [
        potion,
        high_potion,
        super_potion,
        elixer,
        mega_elixer,
        grenade
    ]

main()

