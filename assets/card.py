# card.py
class Card:
    def __init__(self, label):
        """
        label: English label for the card. Parenthetical parts indicate alternate
        functions, e.g. "PARASITE (CARNIVORE)". The card exposes a canonical
        base name (used by game logic) and printable option variants for human
        selection.
        """
        self.label = label
        # parse base and optional mode (parenthesis)
        if '(' in label and ')' in label:
            base = label.split('(')[0].strip()
            inner = label.split('(')[1].split(')')[0].strip()
            # treat parenthetical as an alternate standalone mode
            self.options = [base, inner]
        else:
            self.options = [label]

        # chosen index (0 = first option)
        self.chosen_idx = 0

    @property
    def name(self):
        """Return the currently chosen option (used by game logic)."""
        return self.options[self.chosen_idx]

    def choose_mode(self, idx):
        if 0 <= idx < len(self.options):
            self.chosen_idx = idx
            return True
        return False

    def __str__(self):
        # If multiple options, show both variants joined by '/'
        if len(self.options) > 1:
            return '/'.join(self.options)
        return self.options[0]
