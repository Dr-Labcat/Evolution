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
        Calculate available food based on number of players and dice rolls.
        - 2 players: 1d6 + 2
        - 3 players: 2d6
        - 4 players: 2d6 + 2
        - 5+ players: 3d6 + 2 (requires expansions)
        """
        num_players = len([p for p in self.players if p.species])
        
        if num_players == 2:
            return random.randint(1, 6) + 2
        elif num_players == 3:
            return random.randint(1, 6) + random.randint(1, 6)
        else:  # 4 or more
            return random.randint(1, 6) + random.randint(1, 6) + 2

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

        # Interleaved turns: one card per player
        actions_remaining = True
        end_after_human_skip = False
        end_after_ai_skip = False
        while actions_remaining:
            actions_remaining = False
            for p in self.players:
                if not p.hand:
                    continue

                # -----------------
                # Human player
                # -----------------
                if not p.is_ai:
                    print(f"\n{color('=' * 50, BLUE)}")
                    turn_text = p.name + "'s turn"
                    print(f"{color(turn_text, BOLD)}")
                    print(f"{color('=' * 50, BLUE)}")
                    print(f"\n{color('Your hand:', BOLD)}")
                    for idx, card in enumerate(p.hand, 1):
                        print(f"  {idx}: {card}")
                    print()
                    choice = input(color("Play card? Enter card number or 'q' to skip: ", BOLD))
                    if choice.lower() == 'q':
                        # Human chose to end card play: give AIs one final round then stop
                        end_after_human_skip = True
                        self.show_species_state()
                        break
                    
                    actions_remaining = True
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
                                actions_remaining = True
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
                            print(f"Created new species (card {card} used but NOT a trait)")
                            # If the card is a pair trait, ask which species to pair with
                            if card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                                # List species to choose partner. For COOPERATION, prefer own species only.
                                all_species = []
                                # For COOPERATION prefer only player's own other species
                                if card.name == "COOPERATION":
                                    for sp_item in p.species:
                                        if sp_item is not new_sp:
                                            all_species.append((p, sp_item))
                                # If no own candidates (or other pair types), include all species on table
                                if not all_species:
                                    for op in self.players:
                                        for idx_sp, sp_item in enumerate(op.species, 1):
                                            all_species.append((op, sp_item))
                                if all_species:
                                    print("Choose species to pair with:")
                                    for idx_sp, (op, sp_item) in enumerate(all_species, 1):
                                        print(f"{idx_sp}: {op.name} - {sp_item}")
                                    choice_sp = input("Choose partner species number (or 'q' to skip): ")
                                    if choice_sp.isdigit() and 1 <= int(choice_sp) <= len(all_species):
                                        partner_op, partner_sp = all_species[int(choice_sp)-1]
                                        new_sp.pair_partners[partner_sp] = card
                                        partner_sp.pair_partners[new_sp] = card
                                        print(f"Paired {new_sp} with {partner_op.name}'s {partner_sp} for {card.name}.")
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

                # -----------------
                # AI player
                # -----------------
                elif p.is_ai:
                    if random.random() < 0.7:  # AI plays 70% of the time
                        actions_remaining = True
                        opponents = [pl for pl in self.players if pl != p]
                        
                        # Use strategic AI
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
                        
                        # If the card has multiple functions, pick the first mode for now
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
                        
                        # Choose target species strategically
                        target_idx = AIStrategy.choose_target_species(p, card)
                        
                        if target_idx is not None:
                            success = p.play_card(card, p.species[target_idx])
                            # AI: if it's a pair trait, choose a partner species automatically
                            if success and card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                                base_sp = p.species[target_idx]
                                # Prefer own other species
                                if card.name == "COOPERATION":
                                    candidates = [sp for sp in p.species if sp is not base_sp]
                                else:
                                    candidates = [sp for sp in p.species if sp is not base_sp]
                                    # If none, consider other players' species
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
                        # AI chose to skip this round — trigger single final human-only round
                        end_after_ai_skip = True
                        continue
                # end for p in self.players loop
            # show table once after each full cycle of player actions
            self.show_species_state()
            if end_after_human_skip:
                # Final AI-only round: each AI may play one card, then end card play phase
                for ai in [pl for pl in self.players if pl.is_ai]:
                    if not ai.hand:
                        continue
                    # AI chooses a single card to play using strategy
                    opponents = [pl for pl in self.players if pl != ai]
                    hand_with_scores = [(c, AIStrategy.evaluate_trait_value(c, ai, opponents, self.food_bank)) for c in ai.hand]
                    hand_with_scores.sort(key=lambda x: x[1], reverse=True)
                    if hand_with_scores and hand_with_scores[0][1] > -50:
                        card = hand_with_scores[0][0]
                    elif hand_with_scores:
                        card = random.choice(hand_with_scores[:min(3, len(hand_with_scores))])[0]
                    else:
                        card = random.choice(ai.hand)

                    # Play or create species
                    if card.name == "PARASITE":
                        targets = [op for op in opponents if op.species]
                        if targets:
                            target_player = random.choice(targets)
                            target_sp = random.choice(target_player.species)
                            target_sp.apply_parasite()
                            ai.hand.remove(card)
                            continue

                    target_idx = AIStrategy.choose_target_species(ai, card)
                    if target_idx is not None:
                        success = ai.play_card(card, ai.species[target_idx])
                        if success and card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                            base_sp = ai.species[target_idx]
                            # For COOPERATION, only pair with own species
                            if card.name == "COOPERATION":
                                candidates = [sp for sp in ai.species if sp is not base_sp]
                            else:
                                candidates = [sp for sp in ai.species if sp is not base_sp]
                                if not candidates:
                                    for op in self.players:
                                        if op is ai:
                                            continue
                                        candidates.extend(op.species)
                            if candidates:
                                partner_sp = random.choice(candidates)
                                base_sp.pair_partners[partner_sp] = card
                                partner_sp.pair_partners[base_sp] = card
                                print(f"{ai.name} (AI) paired {base_sp} with {partner_sp} for {card.name}.")
                    else:
                        ai.create_species()
                        if card in ai.hand:
                            ai.hand.remove(card)
                        if card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                            new_sp = ai.species[-1]
                            candidates = [sp for sp in ai.species if sp is not new_sp]
                            if not candidates:
                                for op in self.players:
                                    if op is ai:
                                        continue
                                    candidates.extend(op.species)
                            if candidates:
                                partner_sp = random.choice(candidates)
                                new_sp.pair_partners[partner_sp] = card
                                partner_sp.pair_partners[new_sp] = card
                                print(f"{ai.name} (AI) paired {new_sp} with {partner_sp} for {card.name}.")
                break
            if end_after_ai_skip:
                print(color("\nAn AI skipped their action — one final human-only card-play turn remains.", YELLOW))
                # Allow each human one final card-play action, then end phase
                for human in [pl for pl in self.players if not pl.is_ai]:
                    if not human.hand:
                        continue
                    self.show_species_state()
                    print(f"\n--- {human.name}'s final card-play (AI skipped) ---")
                    print("Your hand:")
                    for idx, card in enumerate(human.hand, 1):
                        print(f"{idx}: {card}")
                    choice = input("Play one card? Enter card number or 'q' to skip: ")
                    if choice.lower() == 'q':
                        continue
                    if not choice.isdigit() or int(choice)-1 not in range(len(human.hand)):
                        print("Invalid!")
                        continue
                    card = human.hand[int(choice)-1]

                    # If multi-function card, ask which mode to use
                    if hasattr(card, 'options') and len(card.options) > 1:
                        print("This card has multiple functions:")
                        for mi, mo in enumerate(card.options, 1):
                            print(f"{mi}: {mo}")
                        mchoice = input("Choose function number (or press Enter for default): ")
                        if mchoice.isdigit() and 1 <= int(mchoice) <= len(card.options):
                            card.choose_mode(int(mchoice)-1)
                        else:
                            card.choose_mode(0)

                    # Handle PARASITE specially (accept Russian label as well)
                    if ("ПАРАЗИТ" in card.name) or (card.name == "PARASITE"):
                        opponents = [op for op in self.players if op != human and op.species]
                        if opponents:
                            print("Which opponent species to infect with PARASITE?")
                            for idx, opponent in enumerate(opponents, 1):
                                print(f"{idx}: {opponent.name}")
                            op_choice = input("Choose opponent (or 'q' to cancel): ")
                            if op_choice.lower() == 'q':
                                continue
                            if not op_choice.isdigit():
                                print("Invalid!")
                                continue
                            if int(op_choice)-1 not in range(len(opponents)):
                                print("Invalid opponent!")
                                continue
                            target_player = opponents[int(op_choice)-1]
                            if target_player.species:
                                print("Which species to infect?")
                                for idx, sp in enumerate(target_player.species, 1):
                                    print(f"{idx}: {sp}")
                                sp_choice = input("Choose species: ")
                                if sp_choice.isdigit() and 1 <= int(sp_choice) <= len(target_player.species):
                                    target_sp = target_player.species[int(sp_choice)-1]
                                    target_sp.apply_parasite()
                                    human.hand.remove(card)
                                    print(f"Infected {target_player.name}'s species with PARASITE!")
                                    continue
                        print("Invalid target!")
                        continue

                    # Regular play: choose target species or create new
                    if human.species:
                        target = input(f"Add to species (1-{len(human.species)}) or create new (0)? ")
                        if not target.isdigit():
                            print("Invalid input!")
                            continue
                        target = int(target)
                        if target == 0:
                            human.create_species()
                            if card in human.hand:
                                human.hand.remove(card)
                            print(f"Created new species (card {card} used but NOT a trait)")
                        elif 1 <= target <= len(human.species):
                            success = human.play_card(card, human.species[target-1])
                            if success:
                                print(f"Added {card} to species {target}")
                            else:
                                print("Species already has 3 traits!")
                        else:
                            print("Invalid species number!")
                    else:
                        human.create_species()
                        if card in human.hand:
                            human.hand.remove(card)
                        print(f"Created new species (card {card} used but NOT a trait)")
                break

    # -----------------------------
    # Feeding Phase
    # -----------------------------
    def feeding_phase(self):
        clear_screen(0)
        print(color("=== Feeding Phase ===", GREEN))
        self.food_bank = self.calculate_food_bank()
        print(f"Food available: {self.food_bank} chips")
        
        # Reset FAT TISSUE conversion flag for this phase
        for p in self.players:
            for sp in p.species:
                sp.fat_converted_this_round = False

        actions_remaining = True
        while actions_remaining and self.food_bank > 0:
            actions_remaining = False
            for p in self.players:
                if not p.species or self.food_bank <= 0:
                    continue

                # Unfed species + fed species with FAT TISSUE eligible for conversion
                # SYMBIOSIS: a species with SYMBIOSIS cannot eat until its partner is fed
                def symbiosis_blocked(sp):
                    if not sp.has_trait("SYMBIOSIS"):
                        return False
                    for partner in list(sp.pair_partners.keys()):
                        if not partner.is_fed():
                            return True
                    return False

                unfed_species = [sp for sp in p.species if not sp.is_fed() and not symbiosis_blocked(sp)]
                fat_eligible_species = [sp for sp in p.species if sp.is_fed() and sp.has_trait("FAT TISSUE") and not sp.fat_converted_this_round]
                feedable_species = unfed_species + fat_eligible_species
                if not feedable_species:
                    continue

                # Human turn
                if not p.is_ai:
                    actions_remaining = True
                    # Show full table so player can see AI animals before choosing
                    self.show_species_state()
                    print(f"\n{color('=' * 50, GREEN)}")
                    turn_text = p.name + "'s feeding turn"
                    print(f"{color(turn_text, BOLD)}")
                    print(f"{color('=' * 50, GREEN)}")
                    print(f"Food bank: {color(str(self.food_bank), YELLOW)}")
                    print(f"{color('Feedable species:', BOLD)}")
                    for idx, sp in enumerate(feedable_species, 1):
                        status = color(" (fat)", MAGENTA) if sp.is_fed() and sp.has_trait("FAT TISSUE") else ""
                        print(f"  {color(str(idx) + ':', BOLD)} {sp}{status}")
                    
                    choice = input(f"Feed species 1-{len(feedable_species)} (or 'q' to skip): ")
                    if choice.lower() == 'q':
                        continue
                    if not choice.isdigit() or int(choice)-1 not in range(len(feedable_species)):
                        print("Invalid!")
                        continue
                    
                    sp = feedable_species[int(choice)-1]
                    
                    # If species has GRAZING, offer manual activation to remove 1 from bank (doesn't count as eating)
                    if sp.has_trait("GRAZING"):
                        gchoice = input("Activate GRAZING to remove 1 from bank without feeding (y/N)? ")
                        if gchoice.lower() == 'y':
                            if self.food_bank > 0:
                                self.food_bank -= 1
                                print(color(f"{p.name} activated GRAZING: removed 1 from food bank.", GREEN))
                                # grazing does not feed the species
                                # show updated bank and continue (player may choose again)
                                print(f"Food bank: {color(str(self.food_bank), YELLOW)}")
                                self.show_species_state()
                                actions_remaining = True
                                continue

                    # If already fed and has FAT TISSUE, convert 1 food to 1 fat (food -> fat)
                    if sp.is_fed() and sp.has_trait("FAT TISSUE") and self.food_bank > 0:
                        sp.add_fat_storage(1)
                        sp.fat_converted_this_round = True
                        self.food_bank -= 1
                        print(color(f"{p.name}'s species converted 1 food to fat.", MAGENTA))
                    else:
                        # Normal feeding for unfed species
                        self.feed_species(sp, p)
                    
                    print(f"Food bank: {color(str(self.food_bank), YELLOW)}")
                    # refresh table after feeding
                    self.show_species_state()
                    
                    # COOPERATION: if one animal of player is fed, another OWN animal gets food automatically
                    if sp.has_trait("COOPERATION"):
                        for other_sp in p.species:
                            if other_sp != sp and not other_sp.is_fed() and self.food_bank > 0:
                                other_sp.food += 1
                                self.food_bank -= 1
                                print(color(f"{p.name}'s COOPERATION: {other_sp} also got food!", MAGENTA))
                                print(f"Food bank: {color(str(self.food_bank), YELLOW)}")

                # AI feeds silently
                elif p.is_ai:
                    actions_remaining = True
                    sp = random.choice(feedable_species)
                    
                    # AI may choose to use GRAZING to remove 1 without feeding
                    if sp.has_trait("GRAZING") and self.food_bank > 0 and random.random() < 0.4:
                        self.food_bank -= 1
                        print(color(f"{p.name} (AI) activated GRAZING: removed 1 from food bank.", GREEN))
                        print(f"Food bank: {self.food_bank}")
                        actions_remaining = True
                        continue
                    
                    # If already fed with FAT TISSUE, auto-convert (chance for AI)
                    if sp.is_fed() and sp.has_trait("FAT TISSUE") and self.food_bank > 0 and random.random() < 0.6:
                        sp.add_fat_storage(1)
                        sp.fat_converted_this_round = True
                        self.food_bank -= 1
                    else:
                        self.feed_species(sp, p)
                    
                    print(f"Food bank: {self.food_bank}")
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
        """Remove unfed species and handle starvation."""
        # First, handle PIRACY before extinction
        for pirate in self.players:
            for pirate_sp in pirate.species:
                if pirate_sp.has_trait("PIRACY"):
                    for victim in self.players:
                        if victim == pirate:
                            continue
                        for victim_sp in victim.species:
                            if not victim_sp.is_fed():
                                # Pirate steals from unfed victim
                                stolen = min(1, victim_sp.food)
                                victim_sp.food -= stolen
                                pirate_sp.food += stolen
                                print(f"{pirate.name}'s PIRACY: stole {stolen} food from {victim.name}'s unfed species!")
                                break

        # Then check for extinction
        for p in self.players:
            for sp in p.species[:]:
                if not sp.is_fed():
                    # Try to use FAT TISSUE reserves to survive
                    if sp.has_trait("FAT TISSUE") and sp.fat_storage > 0:
                        needed = sp.get_food_requirement() - sp.food
                        consumed = sp.consume_fat_storage(needed)
                        if consumed > 0:
                            sp.food += consumed
                            print(color(f"{p.name}'s {sp} used {consumed} fat to avoid starvation.", MAGENTA))
                    # SYMBIOSIS: symbiote can't die while symbiont exists
                    if not sp.is_fed():
                        alive_partner = False
                        if sp.has_trait("SYMBIOSIS"):
                            for partner in list(sp.pair_partners.keys()):
                                if partner in partner.owner.species:
                                    alive_partner = True
                                    break
                        if alive_partner:
                            print(color(f"{p.name}'s {sp} is protected by SYMBIOSIS partner and survives despite being unfed.", MAGENTA))
                            continue
                        # still unfed -> extinct
                        print(f"{p.name}'s {sp} went extinct due to starvation!")
                        p.species.remove(sp)
                    else:
                        # Add collected food to player's total
                        p.food_collected += sp.food
            
            # Reset food for next round
            for sp in p.species:
                sp.reset_food()

    # -----------------------------
    # Score Calculation
    # -----------------------------
    def calculate_scores(self):
        """
        Calculate scores according to rules:
        +2 points per survived animal
        +1 point per trait on survived animals
        +1 point for HIGH BODY WEIGHT and CARNIVORE traits
        +2 points per PARASITE on survived animals
        +1 point per food in player's food collection
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
                    
                    # Special bonuses for specific traits
                    if trait.name in ["HIGH BODY WEIGHT", "CARNIVORE"]:
                        total += 1  # +1 bonus for these traits
                    
                    # Parasites are negative (they cost 2 points)
                    if trait.name == "PARASITE":
                        total += 2  # +2 for having parasite (penalty is in food requirement)
            
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
            self.carnivore_attacks()
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
        print(f"\n🎉 {winner[0]} wins with {winner[1]} points!")
