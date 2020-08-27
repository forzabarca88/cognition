from dataclasses import dataclass
from time import sleep
import random


@dataclass
class Sylar(object):
    def __init__(self):
        self.age_hours = 0
        self.hunger = 50
        self.thirst = 50
        self.health = 50
        self.stress = 50
        self.happiness = 50
        self.wealth = 50
        self.fatal = False
        self.life = LifeRunner(self)

    def live(self):
        if self.is_alive():
            self._process_hunger()
            self._process_thirst()
            self._process_wealth()
            self._process_health()
            self._process_bau()
            self._process_fatal()
    
    def fix_value_ranges(self):
        self.hunger = max(self.hunger, 0)
        self.thirst = max(self.thirst, 0)
        self.wealth = max(self.wealth, 0)
        self.health = min(self.health, 100)
        self.happiness = max(min(self.happiness, 100), 0)
        self.stress = max(min(self.stress, 100), 0)

    def is_alive(self):
        if (self.thirst >= 100 or self.hunger >= 100
            or self.health <= 0):
            return False
        return True

    def _process_fatal(self):
        self.fix_value_ranges()
        fatal_val = 10000
        expected_val = random.randint(1, 1000000)
        if expected_val == fatal_val:
            self.health = 0
            self.fatal = True

    def _process_bau(self):
        self.fix_value_ranges()
        self.happiness += random.randint(-10, 10)
        self.stress += random.randint(-10, 10)
        self.age_hours += 1
        self.thirst += 1
        self.hunger += 0.1
        self.health -= 0.01
        
    def _process_thirst(self):
        self.fix_value_ranges()
        if self.thirst > 80:
            self.thirst -= random.randint(0, self.wealth)
            self.stress += random.randint(0, 10)
            self.happiness -= random.randint(0, 5)
            self.wealth -= random.randint(0,1)

    def _process_hunger(self):
        self.fix_value_ranges()
        if self.hunger > 80:
            self.hunger -= random.randint(0, self.wealth)
            self.stress += random.randint(0, 5)
            self.happiness -= random.randint(0, 5)
            self.wealth -= random.randint(1,3)

    def _process_wealth(self):
        if self.wealth < 80:
            self.wealth += (random.randint(0, 2) * random.randint(0, 1))
        if self.wealth < 50:
            self.happiness -= random.randint(0, 5)
            self.stress += random.randint(0, 10)
        else:
            self.happiness += random.randint(0,3)
            self.stress -= random.randint(0, 5)

    def _process_health(self):
        self.fix_value_ranges()
        if self.health < 20:
            val = random.randint(0, self.wealth)
            self.health += val / 2
            self.wealth -= val
        if self.health > 80:
            self.happiness += random.randint(0,3)
            self.stress -= random.randint(0, 5)
        if self.health < 50:
            self.happiness -= random.randint(0,3)

class LifeRunner(object):
    def __init__(self, person):
        self.person = person

    def start(self):
        while self.person.is_alive():
            self.person.live()
            number_of_years = self.person.age_hours / (24 * 365)
            if self.person.age_hours % (24 * 365) == 0:
                print(self.person.__dict__)
            if number_of_years > 150:
                print(f'Success! Sylar is {number_of_years} years old.')
                return None
        print(f'Dead at {self.person.age_hours / (24*365)} years')
        print(self.person.__dict__)


if __name__ == "__main__":
    bro = Sylar()
    bro.life.start()
