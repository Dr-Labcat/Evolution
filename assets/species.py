# species.py
class Species:
    def __init__(self, owner):
        self.owner = owner
        self.population = 1
        self.body_size = 1
        self.traits = []
        self.food = 0  # chips collected this round
        self.fat_storage = 0  # fat tissue storage for next rounds
        self.hibernating = False  # hibernation state
        self.parasite_count = 0  # number of parasites on this species
        self.pair_partners = {}  # for pair traits: {other_species: trait_card}
        self.fat_converted_this_round = False  # track if fat conversion used this round
        self.fat_eligible_this_turn = False  # became fed in previous turn; eligible for fat conversion now

    def add_trait(self, card):
        """Add a trait card to this species (max 3 traits)."""
        if len(self.traits) < 3:
            self.traits.append(card)
            return True
        return False

    def has_trait(self, trait_name):
        """Check if species has a specific trait."""
        return any(t.name == trait_name for t in self.traits)

    def get_trait_names(self):
        """Get list of all trait names on this species."""
        return [t.name for t in self.traits]

    def get_food_requirement(self):
        """
        Calculate how much food this species needs to be fully fed.
        Base requirement is tied to `body_size` (larger bodies need more food).
        Carnivores also require an extra food to be fully satiated.
        Parasites increase requirement by +2 each.
        """
        req = max(1, int(self.body_size))
        # HIGH BODY WEIGHT increases food requirement by 1
        if self.has_trait("HIGH BODY WEIGHT"):
            req += 1
        if self.has_trait("CARNIVORE"):
            req += 1
        req += 2 * self.parasite_count
        return req

    def is_fed(self):
        """Check if species has enough food to survive."""
        return self.food >= self.get_food_requirement()

    def can_be_eaten_by(self, attacker_species):
        """
        Determine if this species can be eaten by a carnivore.
        Returns (can_eat, defense_applies, defense_name)
        """
        trait_names = self.get_trait_names()
        attacker_traits = attacker_species.get_trait_names()
        
        # Attacker must be carnivore
        if "CARNIVORE" not in attacker_traits:
            return False, False, None
        
        # POISONOUS: attacker dies when eating this
        if "POISONOUS" in trait_names:
            return True, True, "POISONOUS"
        
        # SYMBIOSIS: if partner is alive, can't be eaten
        if "SYMBIOSIS" in trait_names and attacker_species in self.pair_partners:
            return False, True, "SYMBIOSIS"
        
        # SWIMMING: can only be eaten by swimming carnivores
        if "SWIMMING" in trait_names:
            if "SWIMMING" not in attacker_traits:
                return False, True, "SWIMMING"
        
        # HIGH BODY WEIGHT: can only be eaten by attacker with HIGH BODY WEIGHT
        if "HIGH BODY WEIGHT" in trait_names:
            if "HIGH BODY WEIGHT" not in attacker_traits:
                return False, True, "HIGH BODY WEIGHT"
        
        # BURROWING: can't be eaten if fed
        if "BURROWING" in trait_names and self.is_fed():
            return False, True, "BURROWING"
        
        # CAMOUFLAGE: can only be eaten by sharp vision carnivores
        if "CAMOUFLAGE" in trait_names:
            if "SHARP VISION" not in attacker_traits:
                return False, True, "CAMOUFLAGE"
        
        # TAIL LOSS: always survives but loses a trait
        if "TAIL LOSS" in trait_names:
            return True, True, "TAIL LOSS"
        
        # RUNNING: 50% chance to escape (needs dice roll)
        if "RUNNING" in trait_names:
            return True, True, "RUNNING"
        
        # Can be eaten
        return True, False, None

    def get_defense_description(self, defense_type):
        """Get human-readable defense description."""
        defenses = {
            "SWIMMING": "Protected by SWIMMING",
            "HIGH BODY WEIGHT": "Protected by HIGH BODY WEIGHT",
            "BURROWING": "Protected by BURROWING (while fed)",
            "CAMOUFLAGE": "Protected by CAMOUFLAGE",
            "SYMBIOSIS": "Protected by SYMBIOSIS partner",
            "POISONOUS": "Will poison attacker!",
            "TAIL LOSS": "Will sacrifice a trait",
            "RUNNING": "Will attempt to run (50% chance)"
        }
        return defenses.get(defense_type, "Unknown defense")

    def apply_parasite(self):
        """Add a parasite to this species."""
        self.parasite_count += 1

    def remove_parasite(self):
        """Remove a parasite from this species."""
        if self.parasite_count > 0:
            self.parasite_count -= 1

    def sacrifice_trait(self):
        """Remove one trait (for TAIL LOSS defense)."""
        if self.traits:
            self.traits.pop(0)
            return True
        return False

    def reset_food(self):
        """Reset food for new round (but keep fat storage)."""
        self.food = 0

    def add_fat_storage(self, amount):
        """Add to fat tissue storage."""
        self.fat_storage += amount

    def consume_fat_storage(self, amount):
        """Use stored fat for feeding."""
        consumed = min(amount, self.fat_storage)
        self.fat_storage -= consumed
        return consumed

    def __str__(self):
        traits_str = ', '.join([t.name for t in self.traits])
        parasite_str = f" Parasites:{self.parasite_count}" if self.parasite_count > 0 else ""
        return f"Body-size:{self.body_size} Food:{self.food}/{self.get_food_requirement()} Fat:{self.fat_storage} Traits:[{traits_str}]{parasite_str}"
