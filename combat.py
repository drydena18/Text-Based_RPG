import pygame
import random
from utils import blood_splatter

class BloodCombatSystem:
    @staticmethod
    def shadow_strike(attacker, defender):
        damage = random.randint(1, 8) + attacker["stats"]["DEX"] // 2
        if "Garnet Shard" in attacker["inventory"]:
            damage += 3

        blood_splatter(defender["hp"] / defender["max_hp"])
        return damage
    
    @staticmethod
    def cast_necromancy(caster, target, spell):
        cost = spell["blood_cost"]
        if caster["hp"] < cost:
            return "Not enough life force!"
        
        caster["hp"] -= cost
        effect = spell["effect"](target)
        return f"Blood ritual complete! {effect}"