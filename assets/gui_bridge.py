# gui_bridge.py - Bridge between text-based game logic and graphical GUI
"""
This module provides functions to update the graphical GUI from the text-based game.
It captures game state and displays it in the tkinter window.
"""

def update_species_display(game_window, players):
    """Update the species table display in the GUI."""
    if not game_window:
        return
    
    display_text = ""
    for player in players:
        color_code = "CYAN" if "AI" not in player.name else "RED"
        display_text += f"\n{'='*45}\n{player.name}\n{'='*45}\n"
        
        if not player.species:
            display_text += "  (No species yet)\n"
        else:
            for idx, species in enumerate(player.species, 1):
                display_text += f"\n  Species #{idx}:\n"
                display_text += f"    Body Size: {species.body_size}\n"
                
                if species.traits:
                    display_text += f"    Traits: {', '.join(t.name for t in species.traits)}\n"
                else:
                    display_text += "    Traits: None\n"
                
                display_text += f"    Food: {species.food}/{species.get_food_requirement()} Fat: {species.fat_storage}\n"
    
    game_window.update_species(display_text)

def update_hand_display(game_window, hand):
    """Update the player's hand display in the GUI."""
    if not game_window:
        return
    
    hand_cards = []
    for card in hand:
        if len(card.options) > 1:
            # Dual-sided card
            hand_cards.append(f"{card.name} / {card.options[1]}")
        else:
            hand_cards.append(card.name)
    
    game_window.update_hand(hand_cards)

def add_message(game_window, message, message_type="info"):
    """Add a message to the GUI message area."""
    if not game_window:
        return
    
    color_map = {
        "info": "cyan",
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "ai": "magenta"
    }
    
    game_window.add_message(message, color_map.get(message_type, "white"))

def get_player_choice(game_window, prompt, options):
    """Show a choice dialog and return the selected index."""
    if not game_window:
        # Fallback to terminal input
        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return choice - 1
            except ValueError:
                pass
        return 0
    
    result = game_window.show_choice_dialog(prompt, options)
    return result if result is not None else 0

def format_species_summary(player, species_idx):
    """Format a species summary for display."""
    species = player.species[species_idx]
    traits_str = ", ".join([t.name for t in species.traits]) if species.traits else "None"
    return f"{player.name}'s Species #{species_idx + 1} (Body: {species.body_size}, Traits: {traits_str})"

def show_feeding_options(game_window, feedable_species):
    """Display feeding options."""
    if not game_window:
        return
    
    options = [f"Species #{idx + 1}: {species.traits}" if species.traits else f"Species #{idx + 1}: (base)" 
               for idx, species in enumerate(feedable_species)]
    add_message(game_window, f"Choose a species to feed: {options}", "info")
