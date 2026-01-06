# main.py
from assets.game import Game

def main():
    print("Welcome to Russian Evolution (text version)!")
    player_names = ["You", "AI_1"]
    game = Game(player_names)
    game.play_game()
if __name__ == "__main__":
    main()
