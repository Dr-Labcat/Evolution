# player.py
from assets.species import Species

class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.hand = []
        self.species = []
        self.food_collected = 0  # Food tokens collected (for scoring)

    def create_species(self):
        sp = Species(self)
        self.species.append(sp)
        return sp

    def play_card(self, card, species=None):
        if species is None:
            species = self.create_species()
        success = species.add_trait(card)
        if success:
            self.hand.remove(card)
            return True
        return False

    def list_species(self):
        for idx, sp in enumerate(self.species, 1):
            print(f"{idx}: {sp}")
