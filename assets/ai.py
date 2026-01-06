# ai.py
import random

class AIStrategy:
    """Strategic AI for Evolution game"""
    
    TRAIT_SYNERGIES = {
        "CARNIVORE": ["SHARP VISION", "HIGH BODY WEIGHT", "RUNNING"],
        "SHARP VISION": ["CARNIVORE"],
        "HIGH BODY WEIGHT": ["CARNIVORE"],
        "SWIMMING": ["SWIMMING"],  # Other swimmers for mutual protection
        "CAMOUFLAGE": ["CAMOUFLAGE"],  # Stack camouflage for protection
        "RUNNING": ["RUNNING"],  # Stack for better escape
        "BURROWING": ["HIBERNATION ABILITY"],
        "GRAZING": ["HIBERNATION ABILITY"],
        "POISONOUS": [],  # Standalone defense
        "TAIL LOSS": ["TAIL LOSS"],  # Multiple traits to sacrifice
    }
    
    DEFENSIVE_TRAITS = ["SWIMMING", "RUNNING", "CAMOUFLAGE", "SHARP VISION", "HIGH BODY WEIGHT", "BURROWING", "TAIL LOSS", "HIBERNATION ABILITY"]
    FEEDING_TRAITS = ["GRAZING", "HIBERNATION ABILITY", "COOPERATION", "SCAVENGER"]
    AGGRESSIVE_TRAITS = ["CARNIVORE", "PIRACY", "POISONOUS", "PARASITE"]
    
    @staticmethod
    def evaluate_trait_value(card, player, opponents, food_bank):
        """
        Evaluate how valuable a trait is in current game state.
        Returns a score (higher = better).
        """
        score = 0
        trait_name = card.name
        
        # Check if we have carnivores in play (threat assessment)
        enemy_carnivores = sum(1 for opp in opponents 
                              for sp in opp.species 
                              if any(t.name == "CARNIVORE" for t in sp.traits))
        
        # Defensive value if enemies have carnivores
        if enemy_carnivores > 0 and trait_name in AIStrategy.DEFENSIVE_TRAITS:
            score += 50
        
        # Offensive value - create carnivore threats
        if trait_name == "CARNIVORE":
            score += 40
        
        # Feeding traits in low food situations
        if food_bank < 3:
            if trait_name == "GRAZING":
                score += 30
            elif trait_name == "HIBERNATION ABILITY":
                score += 25
        
        # Synergy with existing traits
        for sp in player.species:
            existing_traits = [t.name for t in sp.traits]
            if len(sp.traits) < 3:
                if trait_name in AIStrategy.TRAIT_SYNERGIES:
                    for synergy_trait in AIStrategy.TRAIT_SYNERGIES[trait_name]:
                        if synergy_trait in existing_traits:
                            score += 20
                
                # Penalize weak combinations
                if trait_name in AIStrategy.AGGRESSIVE_TRAITS:
                    if len(existing_traits) == 0:
                        score -= 10  # Don't start new species with aggressive traits
        
        # General scoring
        if trait_name == "SCAVENGER":
            score += 15  # Passive income
        
        if trait_name == "POISONOUS":
            score += 25  # Strong defense against carnivores
        
        return score
    
    @staticmethod
    def choose_target_species(player, card):
        """
        Choose which species to add trait to.
        Returns index in player.species or None to create new.
        """
        if not player.species:
            return None
        
        best_target = None
        best_score = -999
        
        for idx, sp in enumerate(player.species):
            if len(sp.traits) >= 3:
                continue  # Can't add more traits
            
            score = 0
            
            # Prefer adding to species that don't have any traits yet
            if len(sp.traits) == 0:
                score += 30
            elif len(sp.traits) == 1:
                score += 20
            else:
                score += 10
            
            # Prefer building carnivore species
            if card.name in ["SHARP VISION", "HIGH BODY WEIGHT"] or "CARNIVORE" in [t.name for t in sp.traits]:
                score += 40
            
            # Prefer building defensive species with defensive traits
            if card.name in AIStrategy.DEFENSIVE_TRAITS and len([t.name for t in sp.traits if t.name in AIStrategy.DEFENSIVE_TRAITS]) > 0:
                score += 25
            
            if score > best_score:
                best_score = score
                best_target = idx
        
        return best_target if best_score > -50 else None

def ai_play(player, game, food_bank):
    """
    Strategic AI decision making.
    """
    if not player.hand or random.random() > 0.85:  # 15% skip chance
        return False
    
    opponents = [p for p in game.players if p != player]
    card = None
    
    # Sort hand by value
    hand_with_scores = []
    for c in player.hand:
        score = AIStrategy.evaluate_trait_value(c, player, opponents, food_bank)
        hand_with_scores.append((c, score))
    
    # Take highest value card with some randomness
    hand_with_scores.sort(key=lambda x: x[1], reverse=True)
    
    if hand_with_scores:
        # 70% pick best, 30% pick random from top 3
        if random.random() < 0.7 and hand_with_scores[0][1] > -50:
            card = hand_with_scores[0][0]
        elif len(hand_with_scores) > 1:
            card = random.choice(hand_with_scores[:min(3, len(hand_with_scores))])[0]
        else:
            card = hand_with_scores[0][0]
    
    if not card:
        card = random.choice(player.hand)
    
    # Special handling for PARASITE
    if card.name == "PARASITE" and opponents:
        # Attack weakest species of strongest opponent
        best_target = None
        for opp in opponents:
            if opp.species:
                if not best_target or len(opp.species) > 0:
                    best_target = opp
        
        if best_target and best_target.species:
            target_sp = min(best_target.species, key=lambda s: len(s.traits))
            target_sp.apply_parasite()
            player.hand.remove(card)
            return True
    
    # Choose target species
    target_idx = AIStrategy.choose_target_species(player, card)
    
    if target_idx is not None:
        success = player.play_card(card, player.species[target_idx])
        return success
    else:
        # Create new species
        player.create_species()
        if card in player.hand:
            player.hand.remove(card)
        return True
