from dataclasses import dataclass
from enum import Enum

from settings import BLEED, BURN, POISON


class EffectType(Enum):
    BLEED = "bleed"
    POISON = "poison"
    BURN = "burn"


@dataclass
class StatusEffect:
    effect_type: EffectType
    damage_per_tick: int
    max_damage_per_tick: int
    tick_interval: int  # ms
    duration: int  # ms
    color: tuple
    current_stack_count: int = 1
    max_stack_count: int = 3
    last_tick_time: int = 0
    start_time: int = 0
    active: bool = True


class EffectManager:
    @staticmethod
    def create_bleed_effect(source_weapon):
        base_damage = source_weapon.bleed_damage
        return StatusEffect(
            effect_type=EffectType.BLEED,
            damage_per_tick=base_damage * 2,
            max_damage_per_tick=base_damage * 6,
            max_stack_count=3,
            tick_interval=2_000,
            duration=14_000,
            color=BLEED,
        )

    @staticmethod
    def create_poison_effect(source_weapon):
        base_damage = source_weapon.poison_damage
        return StatusEffect(
            effect_type=EffectType.POISON,
            damage_per_tick=base_damage,
            max_damage_per_tick=base_damage * 5,
            max_stack_count=5,
            tick_interval=1_000,
            duration=10_000,
            color=POISON,
        )

    @staticmethod
    def create_burn_effect(source_weapon):
        base_damage = 1
        return StatusEffect(
            effect_type=EffectType.BURN,
            damage_per_tick=base_damage,
            max_damage_per_tick=base_damage * 8,
            max_stack_count=4,
            tick_interval=500,
            duration=8_000,
            color=BURN,
        )
