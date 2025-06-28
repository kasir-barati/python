from random import randrange
from random import random
from math import ceil

class Worrier:
    def __init__(self):
        self.power: int = 100
        self.hp: int = 100
        self.defense: int = 100
    
    def attack(self) -> int:
        min_coefficient = ceil(random() * 0.5)
        max_coefficient = ceil(random() * 100)
        return randrange(
            self.power - ceil(self.power / min_coefficient),
            self.power - ceil(self.power / max_coefficient),
        )


class Mage(Worrier):
    def __init__(self):
        super().__init__()
        """
        Wrong usage
        TypeError: descriptor '__init__' of 'super' object needs an argument
        - super.__init__(self)
        """

    def attack(self) -> int:
        return super().attack()
        """
        Wrong usage:
        AttributeError: type object 'super' has no attribute 'attack'
        - return super.attack()
        RecursionError: maximum recursion depth exceeded
        - self.attack()
        """


mage = Mage()
print(mage.attack())