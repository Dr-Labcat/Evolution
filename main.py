# main.py
import tkinter as tk
from tkinter import simpledialog
from assets.game import Game
from assets.gui_window import create_game_window

def main():
    # Create splash window for player selection
    splash = tk.Tk()
    splash.withdraw()  # Hide window temporarily
    splash.title("Russian Evolution")
    
    # Center the dialog
    splash.update_idletasks()
    
    # Show player selection dialog
    num_players = simpledialog.askinteger(
        "Player Selection",
        "Select number of players:\n2 = You vs AI\n3 = You, AI, AI",
        parent=splash,
        minvalue=2,
        maxvalue=3,
        initialvalue=2
    )
    
    splash.destroy()
    
    if num_players is None:
        return
    
    # Create player names
    player_names = ["You"]
    for i in range(1, num_players):
        player_names.append(f"AI_{i}")
    
    # Create main game window
    root, game_window = create_game_window()
    
    # Start game
    game_window.add_message("Starting game...", "cyan")
    root.update()
    
    game = Game(player_names, game_window)
    
    # Run game in a separate thread to keep GUI responsive
    import threading
    def run_game():
        try:
            game.play_game()
            game_window.add_message("Game finished!", "success")
        except Exception as e:
            game_window.add_message(f"Error: {str(e)}", "error")
    
    game_thread = threading.Thread(target=run_game, daemon=True)
    game_thread.start()
    
    # Keep the window running
    root.mainloop()

if __name__ == "__main__":
    main()

