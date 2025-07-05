from dataclasses import dataclass
import random
from typing import List
import sys

MBTI_TYPES = [
    'INTJ', 'INTP', 'ENTJ', 'ENTP',
    'INFJ', 'INFP', 'ENFJ', 'ENFP',
    'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
    'ISTP', 'ISFP', 'ESTP', 'ESFP'
]


@dataclass
class Sylar(object):
    def __init__(self):
        # MBTI personality type
        self.mbti = random.choice(MBTI_TYPES)
        # Core physiological (defaults, will be modified by MBTI below)
        self.age_hours = 0
        self.hunger = 50
        self.thirst = 50
        self.nutrition = 50
        self.sleep = 50
        self.energy = 50
        self.immune = 50
        self.health = 50
        # Psychological
        self.stress = 50
        self.happiness = 50
        self.self_esteem = 50
        self.cognitive = 50
        self.motivation = 50
        self.purpose = 50
        # Social
        self.social = 50
        self.relationships = 50
        self.support = 50
        # Environment
        self.wealth = 50
        self.safety = 50
        self.environment_quality = 50
        # Personality (Big Five)
        self.openness = random.randint(30, 70)
        self.conscientiousness = random.randint(30, 70)
        self.extraversion = random.randint(30, 70)
        self.agreeableness = random.randint(30, 70)
        self.neuroticism = random.randint(30, 70)
        # MBTI-based starting value adjustments
        # E/I: Extraverts start with higher social/energy, introverts with higher cognitive/self_esteem
        if 'E' in self.mbti:
            self.social = random.randint(60, 80)
            self.energy = random.randint(60, 80)
        else:
            self.social = random.randint(35, 55)
            self.energy = random.randint(40, 60)
            self.cognitive = random.randint(60, 80)
            self.self_esteem = random.randint(55, 75)
        # S/N: Sensors start with higher happiness, intuitives with higher cognitive and openness
        if 'S' in self.mbti:
            self.happiness = random.randint(60, 80)
        else:
            self.cognitive = max(self.cognitive, random.randint(60, 80))
            self.openness = random.randint(60, 80)
        # T/F: Thinkers start with higher cognitive, feelers with higher relationships/support/happiness
        if 'T' in self.mbti:
            self.cognitive = max(self.cognitive, random.randint(65, 85))
            self.stress = random.randint(45, 60)
        else:
            self.relationships = random.randint(60, 80)
            self.support = random.randint(60, 80)
            self.happiness = max(self.happiness, random.randint(65, 85))
        # J/P: Judgers start with higher conscientiousness, perceivers with higher openness/purpose
        if 'J' in self.mbti:
            self.conscientiousness = random.randint(65, 85)
        else:
            self.openness = max(self.openness, random.randint(65, 85))
            self.purpose = random.randint(60, 80)
        # Life status
        self.fatal = False
        self.life = LifeRunner(self)
        # Developmental stage
        self.stage = 'child'

    def live(self):
        if self.is_alive():
            self._update_stage()
            self._circadian_rhythm()
            self._process_hunger()
            self._process_thirst()
            self._process_nutrition()
            self._process_sleep()
            self._process_energy()
            self._process_immune()
            self._process_wealth()
            self._process_health()
            self._process_social()
            self._process_cognitive()
            self._process_psychological()
            self._process_environment()
            self._process_bau()
            self._process_fatal()
            self._random_life_events()

    def fix_value_ranges(self):
        # Clamp all values between -50 and 100 for needs, 0-100 for health
        for attr in [
            'hunger', 'thirst', 'nutrition', 'sleep', 'energy', 'immune',
            'stress', 'happiness', 'self_esteem', 'cognitive', 'motivation', 'purpose',
            'social', 'relationships', 'support', 'wealth', 'safety', 'environment_quality']:
            val = getattr(self, attr)
            setattr(self, attr, max(min(val, 100), -50))
        self.health = max(min(self.health, 100), 0)
        for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']:
            val = getattr(self, trait)
            setattr(self, trait, max(min(val, 100), 0))

    def is_alive(self):
        # Only health reaching zero causes death
        if self.health <= 0:
            return False
        return True

    def _process_fatal(self):
        self.fix_value_ranges()
        # Extremely rare fatal event (e.g., accident, sudden illness)
        fatal_val = 10000
        expected_val = random.randint(1, 10000000)  # 10x less likely
        if expected_val == fatal_val:
            self.health = 0
            self.fatal = True

    def _process_bau(self):
        self.fix_value_ranges()
        # General life passage (tuned for realistic lifespan)
        self.happiness += random.randint(-2, 2)
        self.stress += random.randint(-2, 2)
        self.age_hours += 1
        self.thirst += 0.10 + (100 - self.environment_quality) * 0.001
        self.hunger += 0.05 + (100 - self.nutrition) * 0.002
        self.sleep -= 0.10 + (100 - self.energy) * 0.001
        self.energy -= 0.05 + (100 - self.sleep) * 0.002
        self.immune -= 0.001 + self.stress * 0.00002
        # MBTI-based randomness
        if 'E' in self.mbti:
            self.social += random.uniform(0, 0.5)
            self.energy += random.uniform(0, 0.2)
        else:
            self.social -= random.uniform(0, 0.5)
            self.energy += random.uniform(0, 0.1)
        if 'N' in self.mbti:
            self.cognitive += random.uniform(0, 0.2)
        if 'S' in self.mbti:
            self.happiness += random.uniform(0, 0.2)
        if 'T' in self.mbti:
            self.stress += random.uniform(0, 0.2)
        if 'F' in self.mbti:
            self.happiness += random.uniform(0, 0.2)
        if 'J' in self.mbti:
            self.wealth += random.uniform(0, 0.2)
        if 'P' in self.mbti:
            self.stress += random.uniform(0, 0.2)
        # Only penalize health if needs are very low
        health_penalty = 0
        if self.thirst <= -25:
            health_penalty += 0.05
        if self.hunger <= -25:
            health_penalty += 0.05
        if self.sleep <= -25:
            health_penalty += 0.05
        if self.immune <= -25:
            health_penalty += 0.05
        if self.safety <= -25:
            health_penalty += 0.05
        # Age-based health/energy effects
        years = self.age_hours / (24 * 365)
        if years < 12:  # child
            age_health_mod = -0.01
            age_energy_mod = -0.01
        elif years < 20:  # adolescent
            age_health_mod = 0.0
            age_energy_mod = 0.0
        elif years < 65:  # adult
            age_health_mod = 0.01
            age_energy_mod = 0.01
        else:  # elderly
            # Add randomness to elderly health decay
            base_decay = -0.0015
            random_decay = random.uniform(-0.0005, 0.002)
            age_health_mod = base_decay + random_decay
            age_energy_mod = -0.02
        self.health += age_health_mod
        self.energy += age_energy_mod
        # Base health decay is almost zero
        self.health -= (0.0001 + self.stress * 0.000005 + health_penalty)

    def _process_thirst(self):
        self.fix_value_ranges()
        if self.thirst > 80:
            drink = min(self.wealth, random.randint(3, 12))
            self.thirst -= drink
            self.stress += random.randint(0, 5)
            self.happiness -= random.randint(0, 3)
            self.wealth -= random.randint(0, 1)

    def _process_hunger(self):
        self.fix_value_ranges()
        if self.hunger > 80:
            food = min(self.wealth, random.randint(3, 12))
            self.hunger -= food
            self.nutrition += food * 0.7
            self.stress += random.randint(0, 3)
            self.happiness -= random.randint(0, 3)
            self.wealth -= random.randint(1, 3)
    def _process_nutrition(self):
        self.fix_value_ranges()
        if self.nutrition < 30:
            self.health -= (30 - self.nutrition) * 0.02
            self.immune -= (30 - self.nutrition) * 0.01
            self.stress += 1
        if self.nutrition > 80:
            self.health += (self.nutrition - 80) * 0.02
            self.energy += 1.5
    def _process_sleep(self):
        self.fix_value_ranges()
        if self.sleep < 30:
            self.energy -= (30 - self.sleep) * 0.04
            self.cognitive -= (30 - self.sleep) * 0.04
            self.stress += 1
        if self.sleep > 80:
            self.energy += (self.sleep - 80) * 0.08
    def _process_energy(self):
        self.fix_value_ranges()
        if self.energy < 30:
            self.cognitive -= (30 - self.energy) * 0.04
            self.motivation -= 0.5
            self.stress += 0.5
        if self.energy > 80:
            self.motivation += 1
    def _process_immune(self):
        self.fix_value_ranges()
        if self.immune < 30:
            self.health -= (30 - self.immune) * 0.03
            self.stress += 0.5
        if self.immune > 80:
            self.health += (self.immune - 80) * 0.08

    def _process_wealth(self):
        if self.wealth < 80:
            self.wealth += (random.randint(0, 2) * random.randint(0, 1))
        if self.wealth < 50:
            self.happiness -= random.randint(0, 5)
            self.stress += random.randint(0, 10)
            self.safety -= 1
        else:
            self.happiness += random.randint(0,3)
            self.stress -= random.randint(0, 5)
            self.safety += 1

    def _process_health(self):
        self.fix_value_ranges()
        # Allow health to recover even at moderate levels
        if self.health < 80:
            val = random.randint(0, max(0, int(self.wealth)))
            self.health += val / 0.8  # much stronger recovery
            self.wealth -= val
            self.stress += 0.5
        if self.health > 90:
            self.happiness += random.randint(0,3)
            self.stress -= random.randint(0, 2)
        if self.health < 50:
            self.happiness -= random.randint(0,2)
            self.motivation -= 0.5
    def _process_social(self):
        self.fix_value_ranges()
        # Social support and relationships
        if self.social < 30:
            self.stress += 2
            self.happiness -= 2
            self.self_esteem -= 1
        if self.relationships < 30:
            self.stress += 2
            self.happiness -= 2
        if self.support < 30:
            self.stress += 2
            self.immune -= 1
        if self.social > 80 or self.relationships > 80:
            self.happiness += 2
            self.self_esteem += 1
    def _process_cognitive(self):
        self.fix_value_ranges()
        # Cognitive stimulation
        if self.cognitive < 30:
            self.motivation -= 1
            self.happiness -= 1
        if self.cognitive > 80:
            self.motivation += 1
            self.happiness += 1
    def _process_psychological(self):
        self.fix_value_ranges()
        # Self-determination theory: autonomy, competence, relatedness
        autonomy = self.wealth + self.safety + self.self_esteem
        competence = self.cognitive + self.motivation
        relatedness = self.social + self.relationships + self.support
        self.happiness += (autonomy + competence + relatedness) / 1000
        # Big Five: neuroticism increases stress, extraversion increases social
        self.stress += (self.neuroticism - 50) * 0.01
        self.social += (self.extraversion - 50) * 0.01
        self.cognitive += (self.openness - 50) * 0.01
    def _process_environment(self):
        self.fix_value_ranges()
        # Environment quality affects health, stress
        if self.environment_quality < 30:
            self.health -= 1
            self.stress += 2
        if self.environment_quality > 80:
            self.health += 0.5
            self.stress -= 1
    def _circadian_rhythm(self):
        # Simulate circadian rhythm for sleep/energy
        hour = self.age_hours % 24
        if 22 <= hour or hour < 6:
            self.sleep += 1.5
            self.energy += 0.5
        else:
            self.sleep -= 0.5
            self.energy -= 0.2
    def _update_stage(self):
        # Developmental stages
        years = self.age_hours / (24 * 365)
        if years < 12:
            self.stage = 'child'
        elif years < 20:
            self.stage = 'adolescent'
        elif years < 65:
            self.stage = 'adult'
        else:
            self.stage = 'elderly'
    def _random_life_events(self):
        # Random positive/negative life events
        event_chance = random.random()
        if event_chance < 0.0005:
            # Major positive event
            self.happiness += 10
            self.wealth += 10
        elif event_chance > 0.9995:
            # Major negative event (less frequent, less damaging)
            self.stress += 5
            self.health -= 5


class LifeRunner(object):
    def __init__(self, person):
        self.person = person

    def start(self):
        while self.person.is_alive():
            self.person.live()
            number_of_years = self.person.age_hours / (24 * 365)
            if self.person.age_hours % (24 * 365) == 0:
                print(f"Year {int(number_of_years)}: {self.person.__dict__}")
                sys.stdout.flush()
            if number_of_years > 150:
                print(f'Success! Sylar is {number_of_years} years old.')
                sys.stdout.flush()
                return None
        print(f'Dead at {self.person.age_hours / (24*365)} years')
        print(self.person.__dict__)
        # Find the most depleted critical factor
        criticals = {
            'health': self.person.health,
            'hunger': self.person.hunger,
            'thirst': self.person.thirst,
            'sleep': self.person.sleep,
            'immune': self.person.immune,
            'safety': self.person.safety
        }
        lowest = min(criticals, key=criticals.get)
        print(f"Biggest factor contributing to death: {lowest} (value: {criticals[lowest]})")
        sys.stdout.flush()

if __name__ == "__main__":
    bro = Sylar()
    print(f"Sylar's MBTI personality type: {bro.mbti}")
    sys.stdout.flush()
    bro.life.start()
