from dataclasses import dataclass
from typing import Dict, List, Type

from weapons import BloodScytheWeapon


@dataclass
class EvolutionRecipe:
    base_weapon: str
    result_weapon: str
    required_elements: List[str]
    required_level: int = 1


class EvolutionManager:
    def __init__(self):
        self.recipes: Dict[str, List[EvolutionRecipe]] = {}
        self.weapon_classes: Dict[str, Type] = {}
        self._setup_recipes()
        self._setup_weapon_classes()

    def _setup_recipes(self):
        recipes = [
            # ("scythe", "inferno_scythe", ["fire"], 3),
            ("scythe", "blood_scythe", ["blood"], 1),
            # ("scythe", "demonic_scythe", ["fire", "blood"], 5),
            # ("magic_bullet", "fire_bullet", ["fire"], 2),
            # ("magic_bullet", "inferno_bullet", ["fire", "wind"], 4),
            # ("aura", "blood_aura", ["blood"], 2),
            # ("aura", "toxic_aura", ["toxic"], 2),
        ]

        for base, result, elements, level in recipes:
            if base not in self.recipes:
                self.recipes[base] = []
            self.recipes[base].append(
                EvolutionRecipe(base, result, elements, level)
            )

    def _setup_weapon_classes(self):
        self.weapon_classes = {
            # "inferno_scythe": InfernoScytheWeapon,
            "blood_scythe": BloodScytheWeapon,
            # "demonic_scythe": DemonicScytheWeapon,
            # "fire_bullet": FireBulletWeapon,
            # "inferno_bullet": InfernoBulletWeapon,
            # "blood_aura": BloodAuraWeapon,
            # "toxic_aura": ToxicAuraWeapon,
        }

    def check_evolutions(self, player) -> List[tuple]:
        evolutions = []
        element_names = [e.name for e in player.elements]

        for weapon_name, weapon in player.weapons.items():
            if weapon_name not in self.recipes:
                continue

            for recipe in self.recipes[weapon_name]:
                if not all(
                    e in element_names for e in recipe.required_elements
                ):
                    continue

                if weapon.level < recipe.required_level:
                    continue

                if weapon.__class__.__name__.lower() == recipe.result_weapon:
                    continue

                evolutions.append((weapon, recipe))

        return evolutions

    def apply_evolution(self, player, weapon, recipe) -> bool:
        if recipe.result_weapon not in self.weapon_classes:
            return False

        new_weapon_class = self.weapon_classes[recipe.result_weapon]
        new_weapon = new_weapon_class()
        new_weapon.owner = player
        new_weapon.level = weapon.level  # Сохраняем уровень

        player.weapons[weapon.name] = new_weapon

        return True
