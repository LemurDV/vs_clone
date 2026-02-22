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
        return StatusEffect(
            effect_type=EffectType.BLEED,
            damage_per_tick=source_weapon.bleed_damage,
            max_damage_per_tick=source_weapon.bleed_damage * 3,
            tick_interval=2_000,
            duration=20_000,
            color=BLEED,
        )

    @staticmethod
    def create_poison_effect(source_weapon):
        return StatusEffect(
            effect_type=EffectType.POISON,
            damage_per_tick=source_weapon.poison_damage,
            max_damage_per_tick=source_weapon.bleed_damage * 3,
            tick_interval=2_000,
            duration=20_000,
            color=POISON,
        )

    @staticmethod
    def create_burn_effect(source_weapon):
        return StatusEffect(
            effect_type=EffectType.BURN,
            damage_per_tick=source_weapon.burn_damage,
            max_damage_per_tick=source_weapon.bleed_damage * 3,
            tick_interval=2_000,
            duration=20_000,
            color=BURN,
        )
