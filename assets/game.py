# game.py
from assets.deck import Deck
from assets.player import Player
from assets.ai import AIStrategy
import random

# simple ANSI colors (works in modern terminals)
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED = "\033[31m"
BLUE = "\033[34m"

def color(text, code):
    return f"{code}{text}{RESET}"

def clear_screen(lines=3):
    """Clear screen by printing newlines (works cross-platform)."""
    print("\n" * lines)

class Game:
    def __init__(self, player_names):
        self.deck = Deck()
        self.deck.build_russian_deck()
        self.players = [Player(name, is_ai=("AI" in name)) for name in player_names]
        # Deal 5 cards to each player at game start and let them create their first species
        for p in self.players:
            p.hand.extend(self.deck.draw(5))
            # keep hand in alphabetical order by current card name
            p.hand.sort(key=lambda c: c.name)

        # Flag to skip the first automatic draw in card play phase (players already have 5)
        self.skip_initial_draw = True

        # Create initial species for each player (silently, no verbose prompts)
        for p in self.players:
            if not p.is_ai:
                # Show hand and ask which card to forfeit (mandatory)
                print(color(f"\n{p.name}, choose a card to forfeit for your starting species:", CYAN))
                for idx, card in enumerate(p.hand, 1):
                    print(f"  {color(str(idx) + ':', BOLD)} {card}")
                while True:
                    choice = input(color("Card number: ", YELLOW))
                    if not choice.isdigit():
                        continue
                    ci = int(choice)
                    if 1 <= ci <= len(p.hand):
                        p.hand.pop(ci-1)
                        p.create_species()
                        break
            else:
                # AI: create species and forfeit random card
                p.create_species()
                if p.hand:
                    p.hand.pop(random.randrange(len(p.hand)))
        
        clear_screen(10)  # Large gap before round starts

        self.round_number = 0
        self.food_bank = 0
        self.game_active = True
        
        clear_screen(15)

    # -----------------------------
    # Food Bank Determination
    # -----------------------------
    def calculate_food_bank(self):
        """
        Calculate available food based on number of players (supports up to 8 per rules):
        2: 1d6 + 2
        3: 2d6
        4: 2d6 + 2
        5: 3d6 + 2
        6: 3d6 + 3
        7: 4d6 + 2
        8+: 4d6 + 4
        """
        num_players = len(self.players)

        def roll(n):
            return sum(random.randint(1, 6) for _ in range(n))

        if num_players == 2:
            return random.randint(1, 6) + 2
        elif num_players == 3:
            return roll(2)
        elif num_players == 4:
            return roll(2) + 2
        elif num_players == 5:
            return roll(3) + 2
        elif num_players == 6:
            return roll(3) + 3
        elif num_players == 7:
            return roll(4) + 2
        else:
            return roll(4) + 4

    def show_species_state(self):
        """Print current species for all players (without revealing hands)."""
        print("\n" + color("="*40, MAGENTA))
        print(color(" Table: Species by Player", BOLD))
        print(color("="*40, MAGENTA))
        for p in self.players:
            header = f"{p.name}:"
            print(color(header, BOLD))
            if p.species:
                for idx, sp in enumerate(p.species, 1):
                    line = f"  {idx}: {sp}"
                    # color player's species differently from AI
                    if p.is_ai:
                        print(color(line, RED))
                    else:
                        print(color(line, CYAN))
            else:
                print("  (no species)")
        print(color("="*40, MAGENTA))

    # -----------------------------
    # Card Play Phase
    # -----------------------------
    def card_play_phase(self):
        clear_screen(0)
        print(color("=== Card Play Phase ===", BLUE))

        # Show deck counts (total fixed at 84)
        try:
            total_cards = self.deck.count()
            print(color(f"Deck: {total_cards}/84 cards remaining", BOLD))
        except Exception:
            pass

        # Draw cards for all players (skip for the very first card-play phase because each player was dealt 5)
        if not getattr(self, 'skip_initial_draw', False):
            for p in self.players:
                draw_count = len(p.species) + 3
                p.hand.extend(self.deck.draw(draw_count))
                # keep hand sorted alphabetically
                p.hand.sort(key=lambda c: c.name)
        else:
            # clear the flag after skipping once
            self.skip_initial_draw = False

        # Show table once at the start of the card-play phase
        self.show_species_state()

        # Interleaved turns: one card per player until all pass
        passed = {p: False for p in self.players}
        while not all(passed.values()):
            for p in self.players:
                # skip players who have already passed
                if passed[p]:
                    continue

                # If no cards left, mark as passed
                if not p.hand:
                    passed[p] = True
                    continue

                # Human player
                if not p.is_ai:
                    print(f"\n{color('=' * 50, BLUE)}")
                    turn_text = p.name + "'s turn"
                    print(f"{color(turn_text, BOLD)}")
                    print(f"{color('=' * 50, BLUE)}")
                    print(f"\n{color('Your hand:', BOLD)}")
                    for idx, card in enumerate(p.hand, 1):
                        print(f"  {idx}: {card}")
                    print()
                    choice = input(color("Play card? Enter card number or 'q' to PASS this phase: ", BOLD))
                    if choice.lower() == 'q':
                        passed[p] = True
                        continue

                    if not choice.isdigit() or int(choice)-1 not in range(len(p.hand)):
                        print("Invalid!")
                        continue

                    card = p.hand[int(choice)-1]
                    # If the card has multiple functions, prompt the human to choose
                    if hasattr(card, 'options') and len(card.options) > 1:
                        print(f"\n{color('This card has multiple functions:', YELLOW)}")
                        for mi, mo in enumerate(card.options, 1):
                            print(f"  {mi}: {mo}")
                        mchoice = input(color("Choose function number (or press Enter for default): ", BOLD))
                        if mchoice.isdigit() and 1 <= int(mchoice) <= len(card.options):
                            card.choose_mode(int(mchoice)-1)
                        else:
                            # default to first
                            card.choose_mode(0)

                    # Check if PARASITE (negative trait to place on opponent)
                    if "ПАРАЗИТ" in card.name or card.name == "PARASITE":
                        print(f"\n{color('Which opponent species to infect with PARASITE?', YELLOW)}")
                        target_player = None
                        for idx, opponent in enumerate([op for op in self.players if op != p], 1):
                            print(f"  {idx}: {opponent.name}")

                        op_choice = input(color("Choose opponent (or 'q' to cancel): ", BOLD))
                        if op_choice.lower() == 'q':
                            continue
                        if not op_choice.isdigit():
                            print("Invalid!")
                            continue

                        opponents = [op for op in self.players if op != p]
                        if int(op_choice)-1 not in range(len(opponents)):
                            print("Invalid opponent!")
                            continue

                        target_player = opponents[int(op_choice)-1]
                        if target_player.species:
                            print(f"\n{color('Which species to infect?', YELLOW)}")
                            for idx, sp in enumerate(target_player.species, 1):
                                print(f"  {idx}: {sp}")
                            sp_choice = input(color("Choose species: ", BOLD))
                            if sp_choice.isdigit() and 1 <= int(sp_choice) <= len(target_player.species):
                                target_sp = target_player.species[int(sp_choice)-1]
                                target_sp.apply_parasite()
                                p.hand.remove(card)
                                msg = f"Infected {target_player.name}'s species with PARASITE!"
                                print(f"\n{color(msg, GREEN)}")
                                continue
                        print("Invalid target!")
                        continue

                    # Choose target
                    if p.species:
                        target = input(color(f"Add to species (1-{len(p.species)}) or create new (0)? ", BOLD))
                        if not target.isdigit():
                            print("Invalid input!")
                            continue
                        target = int(target)
                        if target == 0:
                            # Create new species; remove card manually
                            new_sp = p.create_species()
                            if card in p.hand:
                                p.hand.remove(card)
                            print(f"Created new species (card {card} discarded, not a trait)")
                            # Note: Pair cards (SYMBIOSIS, COOPERATION, COMMUNICATION) only create a pairing
                            # when added to an EXISTING species. Creating a new species with them just
                            # discards the card.
                        elif 1 <= target <= len(p.species):
                            success = p.play_card(card, p.species[target-1])
                            if success:
                                print(f"Added {card} to species {target}")
                                # If it's a pair trait, ask which species to pair with
                                if card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                                    base_sp = p.species[target-1]
                                    all_species = []
                                    for op in self.players:
                                        for idx_sp, sp_item in enumerate(op.species, 1):
                                            # show all species except the base species
                                            if sp_item is base_sp:
                                                continue
                                            all_species.append((op, sp_item))
                                    if all_species:
                                        # For COOPERATION prefer own species only
                                        if card.name == "COOPERATION":
                                            own_candidates = [(p, sp_item) for sp_item in p.species if sp_item is not base_sp]
                                            if own_candidates:
                                                all_species = own_candidates
                                        print("Choose species to pair with:")
                                        for idx_sp, (op, sp_item) in enumerate(all_species, 1):
                                            print(f"{idx_sp}: {op.name} - {sp_item}")
                                        choice_sp = input("Choose partner species number (or 'q' to skip): ")
                                        if choice_sp.isdigit() and 1 <= int(choice_sp) <= len(all_species):
                                            partner_op, partner_sp = all_species[int(choice_sp)-1]
                                            base_sp.pair_partners[partner_sp] = card
                                            partner_sp.pair_partners[base_sp] = card
                                            print(f"Paired {base_sp} with {partner_op.name}'s {partner_sp} for {card.name}.")
                            else:
                                print("Species already has 3 traits!")
                        else:
                            print("Invalid species number!")
                    else:
                        # No species yet: must create new
                        p.create_species()
                        if card in p.hand:
                            p.hand.remove(card)
                        print(f"Created new species (card {card} used but NOT a trait)")

                # AI player
                elif p.is_ai:
                    # Simple AI: decide whether to play or pass
                    if random.random() < 0.7 and p.hand:
                        # AI plays a card this round
                        opponents = [pl for pl in self.players if pl != p]
                        card = None
                        hand_with_scores = []
                        for c in p.hand:
                            score = AIStrategy.evaluate_trait_value(c, p, opponents, self.food_bank)
                            hand_with_scores.append((c, score))
                        hand_with_scores.sort(key=lambda x: x[1], reverse=True)
                        if hand_with_scores and hand_with_scores[0][1] > -50:
                            card = hand_with_scores[0][0]
                        elif hand_with_scores:
                            card = random.choice(hand_with_scores[:min(3, len(hand_with_scores))])[0]
                        else:
                            card = random.choice(p.hand)

                        if hasattr(card, 'options') and len(card.options) > 1:
                            card.choose_mode(0)

                        # Handle PARASITE specially
                        if ("ПАРАЗИТ" in card.name or card.name == "PARASITE") and opponents:
                            target_player = random.choice([op for op in opponents if op.species])
                            if target_player and target_player.species:
                                target_sp = random.choice(target_player.species)
                                target_sp.apply_parasite()
                                p.hand.remove(card)
                                continue

                        target_idx = AIStrategy.choose_target_species(p, card)
                        if target_idx is not None:
                            success = p.play_card(card, p.species[target_idx])
                            # AI pair traits
                            if success and card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                                base_sp = p.species[target_idx]
                                candidates = [sp for sp in p.species if sp is not base_sp]
                                if not candidates:
                                    for op in self.players:
                                        if op is p:
                                            continue
                                        candidates.extend(op.species)
                                if candidates:
                                    partner_sp = random.choice(candidates)
                                    base_sp.pair_partners[partner_sp] = card
                                    partner_sp.pair_partners[base_sp] = card
                                    print(f"{p.name} (AI) paired {base_sp} with {partner_sp} for {card.name}.")
                        else:
                            p.create_species()
                            if card in p.hand:
                                p.hand.remove(card)
                    else:
                        passed[p] = True
                        continue

            # show table once after each full cycle of player actions
            self.show_species_state()

    # -----------------------------
    # Feeding Phase
    # -----------------------------
    def feeding_phase(self):
        """
        Feeding phase per official rules:
        - Players take turns in feeding rounds
        - On your turn you choose ONE action:
          1. Take 1 red token from food bank and place on an unfed animal (or on FAT TISSUE if fed)
          2. Use a trait ability (e.g., convert FAT to blue token)
          3. Attack with Predator (gain 2 blue tokens instead of taking red)
        - Fed condition: animal has tokens >= food_requirement
        - A fed animal CANNOT take more red tokens, but CAN take food to FAT TISSUE
        - Feeding ends when all animals are fed + FAT full, or food supply exhausted
        """
        clear_screen(0)
        print(color("=== Feeding Phase ===", GREEN))
        self.food_bank = self.calculate_food_bank()
        print(f"Food available: {color(str(self.food_bank), YELLOW)} red tokens")
        
        # Feeding rounds loop
        feeding_active = True
        while feeding_active and self.food_bank > 0:
            feeding_active = False
            
            for p in self.players:
                # Check if this player has actions available
                unfed = [sp for sp in p.species if sp.food < sp.get_food_requirement()]
                can_use_fat = [sp for sp in p.species if sp.has_trait("FAT TISSUE") and sp.fat_storage < sp.fat_capacity()]
                can_attack = [sp for sp in p.species if sp.has_trait("CARNIVORE") and not sp.predator_used]
                
                # Skip if player has nothing to do
                if not unfed and not can_use_fat and not can_attack:
                    continue
                
                feeding_active = True
                
                if not p.is_ai:
                    # Human player
                    self.show_species_state()
                    print(f"\n{color('=' * 50, GREEN)}")
                    turn_text = p.name + "'s feeding turn"
                    print(color(turn_text, BOLD))
                    print(f"{color('=' * 50, GREEN)}")
                    print(f"Food bank: {color(str(self.food_bank), YELLOW)} red tokens")
                    
                    # Display available actions
                    print(color("Your actions:", BOLD))
                    if unfed:
                        print("  1: Take 1 red token for an unfed animal")
                    else:
                        print("  1: (no unfed animals)")
                    if can_use_fat:
                        print("  2: Convert FAT to blue token (or take red to FAT)")
                    else:
                        print("  2: (no FAT to convert)")
                    if can_attack:
                        print("  3: Attack with Predator")
                    else:
                        print("  3: (no Predators available)")
                    
                    action = input("Choose action (1-3) or 'q' to skip: ")
                    if action.lower() == 'q':
                        # Check mandatory feeding rule
                        if unfed and self.food_bank > 0:
                            print(color("You have unfed animals and food is available — you must act!", YELLOW))
                            continue
                        else:
                            continue
                    
                    if action == '1' and unfed:
                        # Take red token for unfed animal
                        print("\nFed animals:")
                        for idx, sp in enumerate(unfed, 1):
                            req = sp.get_food_requirement()
                            print(f"  {idx}: {sp} (needs {req - sp.food} more)")
                        choice = input(f"Choose 1-{len(unfed)} (or 'q'): ")
                        if choice.lower() == 'q':
                            continue
                        if not choice.isdigit() or int(choice)-1 >= len(unfed):
                            print("Invalid")
                            continue
                        sp = unfed[int(choice)-1]
                        sp.food += 1
                        self.food_bank -= 1
                        sp.received_red = True
                        print(color(f"{p.name}'s {sp} received 1 red token.", GREEN))
                        
                    elif action == '2' and can_use_fat:
                        # Convert FAT or take red to FAT
                        print("\nSpecies with FAT:")
                        for idx, sp in enumerate(can_use_fat, 1):
                            print(f"  {idx}: {sp} (FAT {sp.fat_storage}/{sp.fat_capacity()})")
                        choice = input(f"Choose 1-{len(can_use_fat)} (or 'q'): ")
                        if choice.lower() == 'q':
                            continue
                        if not choice.isdigit() or int(choice)-1 >= len(can_use_fat):
                            print("Invalid")
                            continue
                        sp = can_use_fat[int(choice)-1]
                        
                        # Sub-choice: convert FAT to blue or take red to FAT
                        if sp.fat_storage > 0:
                            subaction = input("  (1) Convert 1 FAT to blue token, or (2) Take red to FAT?: ")
                            if subaction == '1':
                                sp.fat_storage -= 1
                                sp.food += 1
                                print(color(f"{p.name}'s {sp} converted 1 FAT to blue token.", MAGENTA))
                            elif subaction == '2' and self.food_bank > 0:
                                sp.fat_storage += 1
                                self.food_bank -= 1
                                sp.received_red = True
                                print(color(f"{p.name}'s {sp} stored 1 red token as FAT.", MAGENTA))
                        else:
                            if self.food_bank > 0:
                                sp.fat_storage += 1
                                self.food_bank -= 1
                                sp.received_red = True
                                print(color(f"{p.name}'s {sp} stored 1 red token as FAT.", MAGENTA))
                        
                    elif action == '3' and can_attack:
                        # Predator attack
                        print("\nYour Predators:")
                        for idx, sp in enumerate(can_attack, 1):
                            print(f"  {idx}: {sp}")
                        choice = input(f"Choose 1-{len(can_attack)} (or 'q'): ")
                        if choice.lower() == 'q':
                            continue
                        if not choice.isdigit() or int(choice)-1 >= len(can_attack):
                            print("Invalid")
                            continue
                        attacker = can_attack[int(choice)-1]
                        
                        # Find targets
                        targets = []
                        for other_p in self.players:
                            for other_sp in other_p.species:
                                if other_sp is attacker:
                                    continue
                                # Can eat unprotected animals
                                can_eat, has_defense, defense = other_sp.can_be_eaten_by(attacker)
                                if can_eat:
                                    targets.append((other_p, other_sp))
                        
                        if not targets:
                            print("No valid targets.")
                            continue
                        
                        print("\nTargets:")
                        for idx, (other_p, sp) in enumerate(targets, 1):
                            print(f"  {idx}: {other_p.name} - {sp}")
                        tchoice = input(f"Choose 1-{len(targets)} (or 'q'): ")
                        if tchoice.lower() == 'q':
                            continue
                        if not tchoice.isdigit() or int(tchoice)-1 >= len(targets):
                            print("Invalid")
                            continue
                        
                        defender_p, defender_sp = targets[int(tchoice)-1]
                        print(color(f"{p.name}'s Predator ate {defender_p.name}'s {defender_sp}!", MAGENTA))
                        defender_p.species.remove(defender_sp)
                        attacker.food += 2
                        attacker.predator_used = True
                else:
                    # AI turn — simple logic
                    if unfed:
                        sp = random.choice(unfed)
                        sp.food += 1
                        self.food_bank -= 1
                        sp.received_red = True
                    elif can_use_fat:
                        sp = random.choice(can_use_fat)
                        if self.food_bank > 0:
                            sp.fat_storage += 1
                            self.food_bank -= 1
                            sp.received_red = True
                    elif can_attack:
                        attacker = random.choice(can_attack)
                        targets = []
                        for other_p in self.players:
                            for other_sp in other_p.species:
                                if other_sp is not attacker:
                                    can_eat, _, _ = other_sp.can_be_eaten_by(attacker)
                                    if can_eat:
                                        targets.append((other_p, other_sp))
                        if targets:
                            defender_p, defender_sp = random.choice(targets)
                            defender_p.species.remove(defender_sp)
                            attacker.food += 2
                            attacker.predator_used = True

        
        # Reset FAT storage flags after feeding for extinction phase
        for p in self.players:
            for sp in p.species:
                sp.predator_used = False

    def feed_species(self, species, player):
        """Feed a single species from food bank."""
        if self.food_bank <= 0:
            return False
        
        needed = species.get_food_requirement() - species.food
        if needed <= 0:
            return False
        
        # HIBERNATION ABILITY: can be marked as fed without using food bank
        if species.has_trait("HIBERNATION ABILITY"):
            if not species.hibernating:
                species.hibernating = True
                print(color(f"{player.name}'s species entered HIBERNATION (fed without food)", MAGENTA))
                return True

        # FAT TISSUE: use stored fat first if available
        if species.has_trait("FAT TISSUE") and species.fat_storage > 0:
            consumed = species.consume_fat_storage(needed)
            if consumed > 0:
                species.food += consumed
                needed -= consumed
                print(color(f"{player.name}'s species used {consumed} fat from FAT TISSUE instead of bank food.", MAGENTA))
                if needed <= 0:
                    # fully fed by fat
                    return True

        # PARASITE: species with parasites may only take 1 food per turn from the bank
        if species.parasite_count > 0:
            amount = min(1, needed, self.food_bank)
        else:
            # Standard feeding from food bank (may take multiple)
            amount = min(needed, self.food_bank)

        species.food += amount
        self.food_bank -= amount
        print(f"{player.name}'s species took {amount} food from the bank.")

        return True

    # -----------------------------
    # Carnivore Attacks
    # -----------------------------
    def carnivore_attacks(self):
        clear_screen(0)
        print(color("=== Carnivore Attacks ===", RED))
        for attacker in self.players:
            for attacker_sp in attacker.species[:]:
                if "CARNIVORE" not in [t.name for t in attacker_sp.traits]:
                    continue

                # An animal can only use CARNIVORE once per round
                if getattr(attacker_sp, 'predator_used', False):
                    continue

                # A fully fed carnivore without space in FAT TISSUE cannot attack
                if attacker_sp.is_fed() and (not attacker_sp.has_trait("FAT TISSUE") or attacker_sp.fat_storage >= attacker_sp.fat_capacity()):
                    continue

                # Gather viable targets (can_eat == True)
                viable = []
                for defender in self.players:
                    if defender == attacker:
                        continue
                    for defender_sp in defender.species[:]:
                        can_eat, has_defense, defense_type = defender_sp.can_be_eaten_by(attacker_sp)
                        if can_eat:
                            viable.append((defender, defender_sp, has_defense, defense_type))

                if not viable:
                    continue

                # If attacker is human, let them choose target
                if not attacker.is_ai:
                    self.show_species_state()
                    print(f"\n{attacker.name}, choose target for your CARNIVORE (or 'q' to skip):")
                    for idx, (defender, defender_sp, has_defense, defense_type) in enumerate(viable, 1):
                        desc = defender_sp.get_defense_description(defense_type) if has_defense else "No special defense"
                        print(f"{idx}: {defender.name} - {defender_sp} | Defense: {desc}")
                    choice = input(f"Choose 1-{len(viable)} or 'q': ")
                    if choice.lower() == 'q':
                        continue
                    if not choice.isdigit() or int(choice)-1 not in range(len(viable)):
                        print("Invalid choice, skipping attack.")
                        continue
                    target = viable[int(choice)-1]
                    defender, defender_sp, has_defense, defense_type = target

                    # refresh table after human target selection
                    self.show_species_state()

                    # Resolve defenses for chosen target
                    # MIMICRY: allow defender to choose a different species to be attacked instead
                    if defender_sp.has_trait("MIMICRY"):
                        # Build list of potential redirect targets (all other species on table)
                        all_others = []
                        for op in self.players:
                            for sp_item in op.species:
                                if sp_item is defender_sp:
                                    continue
                                all_others.append((op, sp_item))

                        if all_others:
                            if not defender.is_ai:
                                print(f"{defender.name}: {defender_sp} has MIMICRY. Choose species to redirect attack to (or 'n' to keep current target):")
                                for idx_sp, (op, sp_item) in enumerate(all_others, 1):
                                    print(f"{idx_sp}: {op.name} - {sp_item}")
                                choice = input("Choose number or 'n': ")
                                if choice.isdigit() and 1 <= int(choice) <= len(all_others):
                                    partner_op, partner_sp = all_others[int(choice)-1]
                                    defender = partner_op
                                    defender_sp = partner_sp
                                    print(f"Attack redirected to {defender.name}'s {defender_sp} due to MIMICRY.")
                            else:
                                # AI defender: pick random other species to redirect to
                                partner_op, partner_sp = random.choice(all_others)
                                defender = partner_op
                                defender_sp = partner_sp
                                print(f"{defender.name}'s MIMICRY redirected attack to {defender_sp}.")

                    if defense_type == "RUNNING":
                        roll = random.randint(1, 6)
                        if roll >= 4:
                            print(f"{defender.name}'s species RAN AWAY! (rolled {roll})")
                            continue
                        else:
                            print(f"{defender.name}'s species tried to run but failed (rolled {roll})")

                    elif defense_type == "TAIL LOSS":
                        if defender_sp.sacrifice_trait():
                            print(f"{defender.name}'s species escaped by shedding TAIL, losing one trait")
                            continue

                    elif defense_type == "POISONOUS":
                        print(f"{defender.name}'s POISONOUS species killed the carnivore and itself!")
                        attacker.species.remove(attacker_sp)
                        defender.species.remove(defender_sp)
                        continue

                    # Attack succeeds
                    attacker_sp.food += 2
                    attacker_sp.predator_used = True
                    print(f"{attacker.name}'s CARNIVORE ate {defender.name}'s species and gained 2 food tokens!")
                    defender.species.remove(defender_sp)
                    # SCAVENGER: any other species with SCAVENGER trait gains 1 food token
                    for p_scav in self.players:
                        for sp_scav in p_scav.species:
                            if sp_scav is attacker_sp:
                                continue
                            if sp_scav.has_trait("SCAVENGER"):
                                sp_scav.food += 1
                                print(f"{p_scav.name}'s SCAVENGER activated: {sp_scav} gained 1 food!")

                else:
                    # AI: attack first viable target (keep previous logic simple)
                    defender, defender_sp, has_defense, defense_type = random.choice(viable)

                    if has_defense and defense_type == "RUNNING":
                        roll = random.randint(1, 6)
                        if roll >= 4:
                            continue

                    if has_defense and defense_type == "TAIL LOSS":
                        if defender_sp.sacrifice_trait():
                            continue

                    if has_defense and defense_type == "POISONOUS":
                        print(f"{defender.name}'s POISONOUS species killed the carnivore and itself!")
                        attacker.species.remove(attacker_sp)
                        defender.species.remove(defender_sp)
                        continue

                    attacker_sp.food += 2
                    attacker_sp.predator_used = True
                    print(f"{attacker.name}'s CARNIVORE ate {defender.name}'s species and gained 2 food tokens!")
                    defender.species.remove(defender_sp)
                    # SCAVENGER: any other species with SCAVENGER trait gains 1 food token
                    for p_scav in self.players:
                        for sp_scav in p_scav.species:
                            if sp_scav is attacker_sp:
                                continue
                            if sp_scav.has_trait("SCAVENGER"):
                                sp_scav.food += 1
                                print(f"{p_scav.name}'s SCAVENGER activated: {sp_scav} gained 1 food!")

    # -----------------------------
    # Extinction Check
    # -----------------------------
    def extinction_check(self):
        """Remove unfed species and handle starvation.

        Behaviors implemented per rules:
        - PIRACY steals from unfed species before extinction.
        - FAT TISSUE can be consumed to avoid starvation.
        - SYMBIOSIS protects an unfed species if its partner is alive.
        - Surviving species contribute their collected food to player's pool.
        """



        # Then check for extinction and collect food from survivors
        for p in self.players:
            for sp in p.species[:]:
                # If species is already fed, collect its food
                if sp.is_fed():
                    p.food_collected += sp.food
                    continue

                # Try to use FAT TISSUE to satisfy requirement
                if sp.has_trait("FAT TISSUE") and sp.fat_storage > 0:
                    needed = sp.get_food_requirement() - sp.food
                    consumed = sp.consume_fat_storage(needed)
                    if consumed > 0:
                        sp.food += consumed
                        print(color(f"{p.name}'s {sp} used {consumed} fat to avoid starvation.", MAGENTA))
                # If now fed after fat consumption, collect its food
                if sp.is_fed():
                    p.food_collected += sp.food
                    continue

                # SYMBIOSIS protection check
                alive_partner = False
                if sp.has_trait("SYMBIOSIS"):
                    for partner in list(sp.pair_partners.keys()):
                        if partner in partner.owner.species:
                            alive_partner = True
                            break
                if alive_partner:
                    print(color(f"{p.name}'s {sp} is protected by SYMBIOSIS partner and survives despite being unfed.", MAGENTA))
                    continue

                # Still unfed and unprotected -> extinct
                print(f"{p.name}'s {sp} went extinct due to starvation!")
                p.species.remove(sp)

            # Reset food and per-round flags for the remaining species
            for sp in p.species:
                sp.reset_food()
        # extinction phase ended

    # -----------------------------
    # Score Calculation
    # -----------------------------
    def calculate_scores(self):
        """
        Calculate scores according to rules:
        +2 points per survived animal;
        +1 point per trait on survived animals;
        +1 extra for CARNIVORE and HIGH BODY WEIGHT on surviving animals;
        +2 extra per PARASITE affecting a surviving animal (parasite_count);
        +1 point per food in player's food collection.
        """
        scores = {}
        for p in self.players:
            total = 0

            # Score for animals
            for sp in p.species:
                total += 2  # +2 per animal

                # Score traits
                for trait in sp.traits:
                    total += 1  # +1 per trait
                    if trait.name in ["HIGH BODY WEIGHT", "CARNIVORE"]:
                        total += 1  # +1 bonus for these traits

                # Parasite penalty / bonus per rules: +2 per parasite affecting this animal
                total += 2 * sp.parasite_count

            # Score collected food
            total += p.food_collected

            scores[p.name] = total

        return scores

    # -----------------------------
    # Main Game Loop
    # -----------------------------
    def play_game(self):
        """Play game rounds until deck runs out."""
        while self.game_active:
            self.round_number += 1
            print(f"\n{'='*50}")
            print(f"=== ROUND {self.round_number} ===")
            print(f"={'='*50}")
            
            # Check if deck has enough cards
            if len(self.deck.cards) < 3:
                print("\nDeck running low - this is the final round!")
                self.game_active = False
            
            self.card_play_phase()
            self.feeding_phase()
            self.extinction_check()
            
            if not self.game_active:
                break

        print("\n" + "="*50)
        print("=== GAME OVER ===")
        print("="*50)
        scores = self.calculate_scores()
        print("\nFinal Scores:")
        for name, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            print(f"{name}: {score} points")
        
        winner = max(scores.items(), key=lambda x: x[1])
        print(f"\n{winner[0]} wins with {winner[1]} points!")
