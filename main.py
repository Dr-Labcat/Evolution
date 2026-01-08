# main.py
from assets.game import Game
from assets.gui import clear_screen, print_title, get_numbered_choice

def main():
    clear_screen()
    print_title("🎮 RUSSIAN EVOLUTION 🎮")
    
    # Get number of players
    player_options = ["2 Players (You vs AI)", "3 Players (You, AI, AI)"]
    num_choice = get_numbered_choice(player_options, "Select game mode")
    
    num_players = 2 if num_choice == 0 else 3
    
    # Create player names
    player_names = ["You"]
    for i in range(1, num_players):
        player_names.append(f"AI_{i}")
    
    # Start game
    clear_screen()
    game = Game(player_names)
    game.play_game()

if __name__ == "__main__":
    main()

