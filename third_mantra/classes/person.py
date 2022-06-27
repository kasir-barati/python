from random import randrange
from ..enums.actions import Action
from ..types.magic import Magic


class Person:
    hp: int
    max_hp: int
    mp: int
    max_mp: int
    attack_low: int
    attack_high: int
    defense: int
    magic: list[Magic]
    actions: list[Action]
    
    def __init__(
            self, 
            hp: int, 
            mp: int,
            attack: int,
            defense: int,
            magic: list[Magic]):
        self.attack_high = attack + 10
        self.attack_low = attack - 10
        self.defense = defense
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.max_mp = mp
        self.magic = magic
        self.actions = [Action.ATTACK, Action.MAGIC]
    
    def generate_damage(self):
        return randrange(self.attack_low, self.attack_high)

    def generate_spell_damage(self, magic_spell_index: int):
        magic_spell_damage_low = self.magic[magic_spell_index]["damage"] - 5
        magic_spell_damage_high = self.magic[magic_spell_index]["damage"] + 5

        magic_spell_cost = self.get_spell_cost(magic_spell_index)
        self.reduce_mp(magic_spell_cost)
        
        return randrange(magic_spell_damage_low, magic_spell_damage_high)

    def take_damage(self, damage: int):
        if self.hp == 0:
            # TODO: DBC
            # TODO: unit test
            # TODO: Throw error
            return
        
        self.hp -= damage
        
        if self.hp < 0:
            self.hp = 0

        return self.hp

    def get_hp(self) -> int:
        return self.hp
    
    def get_max_hp(self) -> int:
        return self.max_hp
    
    def get_mp(self) -> int:
        return self.mp
    
    def get_max_mp(self) -> int:
        return self.max_mp

    def reduce_mp(self, mp: int) -> None: 
        self.mp -= mp
    
    def get_spell_name(self, magic_spell_index: int) -> str:
        return  self.magic[magic_spell_index]["name"]

    def get_spell_cost(self, magic_spell_index: int) -> int:
        return  self.magic[magic_spell_index]["cost"]

    def choose_action(self):
        actions_length = len(self.actions)
        indexes = range(1, actions_length)

        print("Actions: ")

        for index, action in zip(indexes, self.actions):
            print(f"{index}: {action.name}")

    def choose_magic(self):
        magic_length = len(self.magic)

        print("Magics: ")

        for index in range(1, magic_length):
            spell_name = self.get_spell_name(index)
            spell_cost = self.get_spell_cost(index)

            print(f"{index}: {spell_name}(cost: {spell_cost})")
