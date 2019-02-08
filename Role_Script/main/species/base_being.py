import random
from main.ui.graphics_beings import displays_beings


class Being:
    def __init__(self, name=None, experience=0):
        # Basic
        self.display = displays_beings.get(name)
        self.name = name.title() if self.display else name

        # Base stats
        self.all_stats = ['experience', 'level', 'max_health', 'max_energy', 'health', 'energy', 'strength', 'agility', 'technique']
        self.stats_to_upgrade = ['health', 'energy', 'strength', 'agility', 'technique']
        self.experience = experience
        self.level = self.calculate_level()
        self._health = {'max': 100, 'current': 100}
        self._energy = {'max': 50, 'current': 50}
        self.strength = 10
        self.agility = 10
        self.technique = 10

        if self.experience:
            self.generate_random_stats()

        # Equipment
        self.equipment = ['body', 'head', 'feet', 'hand_1', 'hand_2']
        self.body = None
        self.head = None
        self.feet = None
        self.hand_1 = None
        self.hand_2 = None

    def stats_to_dict(self):
        return self._attr_to_dict(self.all_stats)

    def equipment_to_dict(self):
        return self._attr_to_dict(self.equipment)

    def _attr_to_dict(self, list_):
        tmp_ = {}
        for key in list_:
            tmp_[key] = getattr(self, key)
        return tmp_

    def _get_max_health(self):
        return self._health.get('max')

    def _set_max_health(self, health):
        self._health['max'] = health

    max_health = property(_get_max_health, _set_max_health)

    def _get_current_health(self):
        return self._health.get('current')

    def _set_current_health(self, health):
        self._health['current'] = health if health > 0 else 0

    health = property(_get_current_health, _set_current_health)

    def _get_max_energy(self):
        return self._energy.get('max')

    def _set_max_energy(self, energy):
        self._energy['max'] = energy

    max_energy = property(_get_max_energy, _set_max_energy)

    def _get_current_energy(self):
        return self._energy.get('current')

    def _set_current_energy(self, energy):
        self._energy['current'] = energy

    energy = property(_get_current_energy, _set_current_energy)

    def calculate_level(self):
        return 1 + self.experience // 100

    def _upgrade_stat(self, stat):
        if stat in ['health', 'energy']:
            stat = 'max_{}'.format(stat)
        getattr(self, '_upgrade_{}'.format(stat))()

    def _upgrade_max_health(self):
        increase = 20
        self.max_health += increase
        self.health += increase

    def _upgrade_max_energy(self):
        increase = 5
        self.max_energy += increase
        self.energy += increase

    def _upgrade_strength(self):
        self.strength += 2

    def _upgrade_agility(self):
        self.agility += 2

    def _upgrade_technique(self):
        self.technique += 2

    def generate_random_stats(self):
        for bonus in range(1, self.level):
            self._upgrade_stat(random.choice(self.stats_to_upgrade))

    def attack(self, defender):
        damage = self.strength + self.calculate_bonus_damage()
        defender.health -= damage
        return damage

    def calculate_bonus_damage(self):
        return int(random.randint(0, self.strength // 3) * self.technique / 10)

    def give_experience(self):
        return self.experience // 10 if self.experience // 10 > 10 else 10
