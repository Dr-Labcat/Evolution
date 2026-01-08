# game.py
from assets.deck import Deck
from assets.player import Player
from assets.ai import AIStrategy
from assets import gui
import random

class Game:
    def __init__(self, player_names, game_window=None):
        self.deck = Deck()
        self.deck.build_russian_deck()
        self.players = [Player(name, is_ai=("AI" in name)) for name in player_names]
        self.game_window = game_window  # Store reference to GUI window
        
        # Deal 5 cards to each player at game start and let them create their first species
        for p in self.players:
            p.hand.extend(self.deck.draw(5))
            # keep hand in alphabetical order by current card name
            p.hand.sort(key=lambda c: c.name)

        # Flag to skip the first automatic draw in card play phase (players already have 5)
        self.skip_initial_draw = True

        # Create initial species for each player (silently, no verbose prompts)
        if self.game_window:
            # Using graphical GUI
            for p in self.players:
                if not p.is_ai:
                    # Ask human player which card to forfeit
                    forfeit_options = [f"{idx+1}. {card.name}" for idx, card in enumerate(p.hand)]
                    forfeit_options.append("Skip (random card)")
                    self.game_window.add_message(f"{p.name}: Choose a card to forfeit for starting species", "cyan")
                    choice = self.get_gui_choice("Card to forfeit:", forfeit_options)
                    p.create_species()
                    if choice < len(p.hand):
                        p.hand.pop(choice)
                    elif p.hand:
                        p.hand.pop(random.randrange(len(p.hand)))
                else:
                    # AI: create species and forfeit random card
                    p.create_species()
                    if p.hand:
                        p.hand.pop(random.randrange(len(p.hand)))
        else:
            # Using terminal GUI
            for p in self.players:
                if not p.is_ai:
                    # Show hand and ask which card to forfeit (mandatory)
                    gui.clear_screen()
                    gui.print_header(f"{p.name}, Choose a Card to Forfeit for Starting Species")
                    gui.show_hand(p.hand)
                    while True:
                        choice = input(gui.console.render_str("[bold cyan]Card number: [/bold cyan]")).strip()
                        if not choice.isdigit():
                            gui.print_error("Please enter a number")
                            continue
                        ci = int(choice)
                        if 1 <= ci <= len(p.hand):
                            p.hand.pop(ci-1)
                            p.create_species()
                            break
                        else:
                            gui.print_error("Invalid choice")
                else:
                    # AI: create species and forfeit random card
                    p.create_species()
                    if p.hand:
                        p.hand.pop(random.randrange(len(p.hand)))
            
            gui.clear_screen()

        self.round_number = 0
        self.food_bank = 0
        self.game_active = True
    
    def update_gui_display(self):
        """Update the graphical GUI with current game state."""
        if not self.game_window:
            return
        
        from assets.gui_bridge import update_species_display, add_message
        
        # Update species table
        update_species_display(self.game_window, self.players)
        
        # Update round and food
        self.game_window.update_round(self.round_number)
        self.game_window.update_food(self.food_bank)
        
        # Update player hand if human player
        human_player = next((p for p in self.players if not p.is_ai), None)
        if human_player:
            self.game_window.update_hand([c.name if len(c.options) <= 1 else f"{c.name}/{c.options[1]}" for c in human_player.hand])
        
        self.game_window.root.update()
    
    def get_gui_choice(self, prompt, options):
        """Get choice from GUI or terminal fallback."""
        if self.game_window:
            result = self.game_window.get_input_sync(prompt, options)
            return result if result is not None else -1
        else:
            for i, opt in enumerate(options, 1):
                print(f"{i}. {opt}")
            while True:
                try:
                    choice = input(f"{prompt}: ")
                    if choice.lower() == 'q':
                        return -1
                    idx = int(choice) - 1
                    if 0 <= idx < len(options):
                        return idx
                except (ValueError, EOFError):
                    pass
    
    def add_gui_message(self, message, msg_type="info"):
        """Add message to GUI or print to terminal."""
        if self.game_window:
            self.game_window.add_message(message, msg_type)
            self.game_window.root.update()
        else:
            print(message)

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
        if self.game_window:
            self.update_gui_display()
        else:
            gui.show_species_table(self.players)

    # -----------------------------
    # Card Play Phase
    # -----------------------------
    def card_play_phase(self):
        gui.clear_screen()
        gui.print_header("Card Play Phase")

        # Show deck counts (total fixed at 84)
        try:
            total_cards = self.deck.count()
            gui.show_deck_count(total_cards, 84)
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
                    if not self.game_window:
                        gui.clear_screen()
                        gui.show_player_turn(p)
                        gui.show_species_table(self.players)
                        gui.show_hand(p.hand)
                    
                    # Create hand display options
                    hand_options = [f"{c.name}" if len(c.options) <= 1 else f"{c.name} / {c.options[1]}" for c in p.hand]
                    hand_options.append("Skip turn")
                    
                    # Update GUI display
                    if self.game_window:
                        self.game_window.add_message(f"Your turn! Choose a card or skip.", "cyan")
                        self.update_gui_display()
                    
                    # Get card choice
                    card_idx = self.get_gui_choice(f"{p.name} - Choose card to play (or skip)", hand_options)
                    
                    if card_idx == len(hand_options) - 1 or card_idx == -1:
                        # Human chose to skip/end card play
                        self.add_gui_message(f"{p.name} skipped their turn", "info")
                        end_after_human_skip = True
                        self.show_species_state()
                        break
                    
                    actions_remaining = True
                    card = p.hand[card_idx]
                    # If the card has multiple functions, prompt the human to choose
                    if hasattr(card, 'options') and len(card.options) > 1:
                        self.add_gui_message(f"This card has multiple functions", "warning")
                        options = [str(opt) for opt in card.options]
                        mode_choice = self.get_gui_choice("Choose card function", options)
                        if mode_choice >= 0:
                            card.choose_mode(mode_choice)
                        else:
                            card.choose_mode(0)
                    
                    # Check if PARASITE (negative trait to place on opponent)
                    if card.name == "PARASITE" or (hasattr(card, 'options') and any('PARASITE' in opt for opt in card.options)):
                        opponents = [op for op in self.players if op != p and op.species]
                        if opponents:
                            opponent_names = [op.name for op in opponents]
                            target_idx = self.get_gui_choice(f"Choose opponent to infect", opponent_names)
                            target_player = opponents[target_idx] if 0 <= target_idx < len(opponents) else None
                            
                            if target_player and target_player.species:
                                species_list = [str(sp) for sp in target_player.species]
                                sp_choice = self.get_gui_choice("Which species to infect", species_list)
                                if 0 <= sp_choice < len(target_player.species):
                                    target_player.species[sp_choice].apply_parasite()
                                    p.hand.remove(card)
                                    self.add_gui_message(f"Infected {target_player.name}'s species with PARASITE!", "success")
                                    actions_remaining = True
                                    continue
                        self.add_gui_message("Invalid target!", "error")
                        continue
                    
                    # Choose target
                    if p.species:
                        choices = [str(sp) for sp in p.species] + ["Create new species"]
                        target = self.get_gui_choice("Add to species or create new", choices)
                        
                        if target == len(p.species):  # Create new
                            new_sp = p.create_species()
                            if card in p.hand:
                                p.hand.remove(card)
                            self.add_gui_message(f"Created new species", "success")
                            # Note: When creating a new species, the card is just consumed to create it
                            # It does NOT become a trait, so no pairing for new species creation
                        elif target is not None and 0 <= target < len(p.species):
                            success = p.play_card(card, p.species[target])
                            if success:
                                self.add_gui_message(f"Added {card.name} to species {target + 1}", "success")
                                # Handle pair traits ONLY when adding to existing species
                                if card.name in ["COMMUNICATION", "SYMBIOSIS", "COOPERATION"]:
                                    base_sp = p.species[target]
                                    all_species = []
                                    for op in self.players:
                                        for sp_item in op.species:
                                            if sp_item is not base_sp:
                                                all_species.append((op, sp_item))
                                    if all_species and card.name == "COOPERATION":
                                        own_candidates = [(p, sp_item) for sp_item in p.species if sp_item is not base_sp]
                                        if own_candidates:
                                            all_species = own_candidates
                                    if all_species:
                                        sp_choices = [f"{op.name} - {sp_item}" for op, sp_item in all_species]
                                        sp_choice = self.get_gui_choice("Choose species to pair with (or skip)", sp_choices + ["Skip pairing"])
                                        if sp_choice >= 0 and sp_choice < len(all_species):
                                            partner_op, partner_sp = all_species[sp_choice]
                                            base_sp.pair_partners[partner_sp] = card
                                            partner_sp.pair_partners[base_sp] = card
                                            self.add_gui_message(f"Paired with {partner_op.name}'s {partner_sp}", "success")
                            else:
                                self.add_gui_message("Species already has 3 traits!", "error")
                    else:
                        # No species yet: must create new
                        p.create_species()
                        if card in p.hand:
                            p.hand.remove(card)
                        self.add_gui_message(f"Created new species", "success")

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
                        if (card.name == "PARASITE" or (hasattr(card, 'options') and any('PARASITE' in opt for opt in card.options))) and opponents:
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
                                    gui.print_info(f"{p.name} (AI) paired {base_sp} with {partner_sp} for {card.name}.")
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
                break
            if end_after_ai_skip:
                break

    # -----------------------------
    # Feeding Phase
    # -----------------------------
    def feeding_phase(self):
        gui.clear_screen()
        gui.print_header("Feeding Phase")
        self.food_bank = self.calculate_food_bank()
        gui.show_food_bank(self.food_bank)
        
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
                    if not self.game_window:
                        gui.show_player_turn(p)
                        gui.show_food_bank(self.food_bank)
                        gui.print_info("Feedable species:")
                        for idx, sp in enumerate(feedable_species, 1):
                            fat_marker = " (can convert to fat)" if sp.is_fed() and sp.has_trait("FAT TISSUE") else ""
                            gui.print_info(f"  {idx}: {sp}{fat_marker}")
                    else:
                        self.add_gui_message(f"Food bank: {self.food_bank}", "info")
                        self.update_gui_display()
                    
                    # Build feedable species options
                    feed_options = []
                    for idx, sp in enumerate(feedable_species):
                        fat_marker = " (fat)" if sp.is_fed() and sp.has_trait("FAT TISSUE") else ""
                        feed_options.append(f"{sp}{fat_marker}")
                    feed_options.append("Skip feeding")
                    
                    choice = self.get_gui_choice(f"Feed species 1-{len(feedable_species)} (or skip)", feed_options)
                    
                    if choice == len(feed_options) - 1 or choice == -1:
                        continue
                    
                    if choice < 0 or choice >= len(feedable_species):
                        self.add_gui_message("Invalid!", "error")
                        continue
                    
                    sp = feedable_species[choice]
                    
                    # If species has GRAZING, offer manual activation to remove 1 from bank (doesn't count as eating)
                    if sp.has_trait("GRAZING"):
                        grazing_options = ["Activate GRAZING (remove 1 food)", "Don't activate GRAZING"]
                        gchoice = self.get_gui_choice("This species has GRAZING", grazing_options)
                        if gchoice == 0:
                            if self.food_bank > 0:
                                self.food_bank -= 1
                                gui.print_success(f"{p.name} activated GRAZING: removed 1 from food bank.")
                                # grazing does not feed the species
                                # show updated bank and continue (player may choose again)
                                gui.show_food_bank(self.food_bank)
                                self.show_species_state()
                                actions_remaining = True
                                continue

                    # If already fed and has FAT TISSUE, convert 1 food to 1 fat (food -> fat)
                    if sp.is_fed() and sp.has_trait("FAT TISSUE") and self.food_bank > 0:
                        sp.add_fat_storage(1)
                        sp.fat_converted_this_round = True
                        self.food_bank -= 1
                        gui.print_info(f"{p.name}'s species converted 1 food to fat.")
                    else:
                        # Normal feeding for unfed species
                        self.feed_species(sp, p)
                    
                    gui.show_food_bank(self.food_bank)
                    # refresh table after feeding
                    self.show_species_state()
                    
                    # COOPERATION: if one animal of player is fed, another OWN animal gets food automatically
                    if sp.has_trait("COOPERATION"):
                        for other_sp in p.species:
                            if other_sp != sp and not other_sp.is_fed() and self.food_bank > 0:
                                other_sp.food += 1
                                self.food_bank -= 1
                                gui.print_success(f"{p.name}'s COOPERATION: {other_sp} also got food!")
                                gui.show_food_bank(self.food_bank)
                    
                    # Mark that actions were taken
                    actions_remaining = True

                # AI feeds silently
                elif p.is_ai:
                    actions_remaining = True
                    sp = random.choice(feedable_species)
                    
                    # AI may choose to use GRAZING to remove 1 without feeding
                    if sp.has_trait("GRAZING") and self.food_bank > 0 and random.random() < 0.4:
                        self.food_bank -= 1
                        gui.print_success(f"{p.name} (AI) activated GRAZING: removed 1 from food bank.")
                        gui.show_food_bank(self.food_bank)
                        continue
                    
                    # If already fed with FAT TISSUE, auto-convert (chance for AI)
                    if sp.is_fed() and sp.has_trait("FAT TISSUE") and self.food_bank > 0 and random.random() < 0.6:
                        sp.add_fat_storage(1)
                        sp.fat_converted_this_round = True
                        self.food_bank -= 1
                    else:
                        self.feed_species(sp, p)
                    
                    gui.show_food_bank(self.food_bank)

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
                gui.print_info(f"{player.name}'s species entered HIBERNATION (fed without food)")
                return True

        # FAT TISSUE: use stored fat first if available
        if species.has_trait("FAT TISSUE") and species.fat_storage > 0:
            consumed = species.consume_fat_storage(needed)
            if consumed > 0:
                species.food += consumed
                needed -= consumed
                gui.print_info(f"{player.name}'s species used {consumed} fat from FAT TISSUE instead of bank food.")
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
        gui.print_info(f"{player.name}'s species took {amount} food from the bank.")

        return True

    # -----------------------------
    # Carnivore Attacks
    # -----------------------------
    def carnivore_attacks(self):
        if not self.game_window:
            gui.clear_screen()
            gui.print_header("Carnivore Attacks")
        
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
                    
                    # Build target options
                    target_options = []
                    for defender, defender_sp, has_defense, defense_type in viable:
                        desc = defender_sp.get_defense_description(defense_type) if has_defense else "No defense"
                        target_options.append(f"{defender.name} - {defender_sp} | {desc}")
                    target_options.append("Skip attack")
                    
                    if self.game_window:
                        self.add_gui_message(f"Choose target for CARNIVORE attack", "warning")
                        self.update_gui_display()
                    
                    choice = self.get_gui_choice(f"Choose attack target (or skip)", target_options)
                    
                    if choice == len(target_options) - 1 or choice == -1:
                        continue
                    if choice < 0 or choice >= len(viable):
                        self.add_gui_message("Invalid choice, skipping attack.", "error")
                        continue
                    target = viable[choice]
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
                                # Build redirect options
                                redirect_options = []
                                for op, sp_item in all_others:
                                    redirect_options.append(f"{op.name} - {sp_item}")
                                redirect_options.append("Keep current target")
                                
                                if self.game_window:
                                    self.add_gui_message(f"{defender_sp} has MIMICRY! Choose redirect target", "warning")
                                
                                choice = self.get_gui_choice(f"Redirect attack to (or keep current)", redirect_options)
                                
                                if choice >= 0 and choice < len(all_others):
                                    partner_op, partner_sp = all_others[choice]
                                    defender = partner_op
                                    defender_sp = partner_sp
                                    self.add_gui_message(f"Attack redirected to {defender.name}'s {defender_sp} by MIMICRY!", "info")
                            else:
                                # AI defender: pick random other species to redirect to
                                partner_op, partner_sp = random.choice(all_others)
                                defender = partner_op
                                defender_sp = partner_sp
                                self.add_gui_message(f"MIMICRY redirected attack to {defender_sp}!", "info")

                    if defense_type == "RUNNING":
                        roll = random.randint(1, 6)
                        if roll >= 4:
                            self.add_gui_message(f"{defender.name}'s species RAN AWAY! (rolled {roll})", "success")
                            continue
                        else:
                            self.add_gui_message(f"{defender.name}'s species tried to run but failed (rolled {roll})", "warning")

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
                            gui.print_info(f"{p.name}'s {sp} used {consumed} fat to avoid starvation.")
                    # SYMBIOSIS: symbiote can't die while symbiont exists
                    if not sp.is_fed():
                        alive_partner = False
                        if sp.has_trait("SYMBIOSIS"):
                            for partner in list(sp.pair_partners.keys()):
                                if partner in partner.owner.species:
                                    alive_partner = True
                                    break
                        if alive_partner:
                            gui.print_info(f"{p.name}'s {sp} is protected by SYMBIOSIS partner and survives despite being unfed.")
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
            
            if not self.game_window:
                gui.clear_screen()
                gui.show_round_header(self.round_number)
            else:
                self.game_window.add_message(f"Starting Round {self.round_number}...", "cyan")
            
            # Check if deck has enough cards
            if len(self.deck.cards) < 3:
                msg = "Deck running low - this is the final round!"
                if self.game_window:
                    self.game_window.add_message(msg, "warning")
                else:
                    gui.print_warning(msg)
                self.game_active = False
            
            self.card_play_phase()
            self.feeding_phase()
            self.carnivore_attacks()
            self.extinction_check()
            self.update_gui_display()
            
            if not self.game_active:
                break

        if self.game_window:
            self.game_window.add_message("Game finished! Calculating scores...", "success")
        else:
            gui.clear_screen()
        
        scores = self.calculate_scores()
        
        # Display final scores
        gui.print_header("GAME OVER - Final Scores")
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for name, score in sorted_scores:
            gui.print_info(f"{name}: {score} points")
        
        winner_name, winner_score = sorted_scores[0]
        gui.show_game_over(self.players[[p.name for p in self.players].index(winner_name)])
