import random

from elements import BloodElement


class ElementManager:
    def __init__(self):
        self.all_elements = []
        self.initialize_elements()

    def initialize_elements(self):
        self.all_elements.extend(
            [
                BloodElement(),
                BloodElement(),
                BloodElement(),
            ]
        )

    def get_random_elements(self, count=3):
        available = self.all_elements.copy()
        selected = []

        while len(selected) < count and available:
            element = random.choice(available)
            available.remove(element)
            selected.append(element)

        return selected

    def add_new_upgrade(self, element):
        self.all_elements.append(element)
