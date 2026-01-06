import random
from assets.card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []

    def build_russian_deck(self):
        """
        Build the 84-card Russian deck according to the provided composition.

        The labels are kept in Russian for display; any parenthetical in the
        label will be treated as an alternate mode (player chooses which mode
        to use when playing the card).
        """
        # English labels mapped from the Russian composition. Parentheticals
        # indicate alternate functions; the canonical base name is used by
        # game logic (e.g., "PARASITE").
        composition = [
            ("CAMOUFLAGE", 4),
            ("BURROWING", 4),
            ("SHARP VISION", 4),
            ("SYMBIOSIS", 4),
            ("PIRACY", 4),
            ("GRAZING", 4),
            ("TAIL LOSS", 4),
            ("HIBERNATION", 4),
            ("POISONOUS", 4),
            ("COMMUNICATION", 4),
            ("SCAVENGER", 4),
            ("RUNNING", 4),
            ("MIMICRY", 4),
            ("SWIMMING", 8),
            ("PARASITE (CARNIVORE)", 4),
            ("PARASITE (FAT TISSUE)", 4),
            ("COOPERATION (CARNIVORE)", 4),
            ("COOPERATION (FAT TISSUE)", 4),
            ("HIGH BODY WEIGHT (CARNIVORE)", 4),
            ("HIGH BODY WEIGHT (FAT TISSUE)", 4),
        ]

        self.cards = []
        for label, count in composition:
            for _ in range(count):
                self.cards.append(Card(label))

        # Safety check: ensure deck size is 84
        total = len(self.cards)
        if total != 84:
            raise ValueError(f"Russian deck build error: expected 84 cards, built {total}")

        random.shuffle(self.cards)

    def draw(self, n=1):
        drawn = []
        for _ in range(n):
            if not self.cards:
                # reshuffle discard into deck
                self.cards = list(self.discard)
                self.discard = []
                random.shuffle(self.cards)
            if self.cards:
                drawn.append(self.cards.pop())
        return drawn

    def discard_cards(self, cards):
        self.discard.extend(cards)

    def count(self):
        return len(self.cards) + len(self.discard)
