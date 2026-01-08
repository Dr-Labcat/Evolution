<<<<<<< HEAD
# Evolution: The Origin of Species - Python Implementation

A faithful digital implementation of the award-winning Russian board game "Evolution: The Origin of Species" by Dmitry Knorre and Sergey Machin.
An attempt at adding a GUI to the working version

## About the Game

**Evolution** is a strategic card game where players create and evolve species to survive in a competitive ecosystem. Each species can develop traits like CARNIVORE (to hunt), SWIMMING (to escape), POISON (for defense), and many more. The player with the most points at the end wins!

**Key Features:**
- 19 unique trait cards representing different evolutionary adaptations
- Dynamic food bank system with dice rolls
- Complex predator-prey interactions with defense mechanics
- Strategic trait combinations and synergies
- Intelligent AI opponents
- 30-60 minute gameplay

## Quick Start

### Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

### Installation
```bash
cd EVOLUTION
python main.py
```

### First Game
1. You'll be playing as "You" against "AI_1"
2. Follow the prompts to play cards and feed species
3. Watch as evolution unfolds!

## File Guide

| File | Purpose |
|------|---------|
| `main.py` | Game entry point |
| `game.py` | Core game logic and flow |
| `player.py` | Player management |
| `species.py` | Species data and trait logic |
| `card.py` | Card/trait representation |
| `deck.py` | Card deck management |
| `ai.py` | Intelligent AI strategy |

## Documentation

- **[HOW_TO_PLAY.md](HOW_TO_PLAY.md)** - Step-by-step gameplay guide
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Trait reference and strategy tips
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details

## Game Rules Summary

### The Basic Idea
1. **Card Play Phase**: Draw and play cards to build species with traits
2. **Feeding Phase**: Roll dice for food, feed your species
3. **Carnivore Attacks**: Predators attack prey with various defenses
4. **Extinction**: Unfed species die, survivors are scored
5. **Repeat** until the deck runs out

### Winning
Most points at the end! Points come from:
- Surviving species (2 points each)
- Traits on survivors (1 point each)
- Food collected (1 point each)
- Special bonuses for certain traits

### Available Traits

**19 Total Traits:**
- **Predatory**: CARNIVORE, SHARP VISION, PIRACY
- **Defensive**: SWIMMING, RUNNING, CAMOUFLAGE, HIGH BODY WEIGHT, BURROWING, TAIL LOSS, POISONOUS
- **Feeding**: GRAZING, HIBERNATION, FAT TISSUE, COOPERATION, COMMUNICATION, SCAVENGER
- **Special**: SYMBIOSIS, MIMICRY, PARASITE

Each trait has unique mechanics and interactions!

## Gameplay Examples

### Example Attack Scenario
```
Your species: SWIMMING
Enemy carnivore: Regular (no SWIMMING)

Result: Your species is protected! 
The regular carnivore can't catch swimmers.
```

### Example Defense Scenario
```
Your species: RUNNING
Enemy carnivore: Attacks
Dice roll: 5 (need 4-6 to escape)

Result: Your species escapes!
```

### Example Feeding Scenario
```
Species A: GRAZING (auto-feeds)
Species B: HIBERNATION (sleeps through round)
Species C: Needs 1 food
Food bank: 2 available

Result: Species A auto-feeds, Species C gets 1,
Species B goes dormant. 2 food used perfectly!
```

## Key Features Implemented

✅ **Complete Trait System** - All 19 traits with full mechanics
✅ **Dynamic Food System** - Dice-based food bank calculation
✅ **Defense Mechanics** - Proper counter-play for all traits
✅ **Intelligent AI** - Strategic decision-making with synergy awareness
✅ **Accurate Scoring** - Matches official rules
✅ **Proper Game Flow** - Ends when deck runs out
✅ **Full Trait Interactions** - Complex combinations work correctly

## Strategy Tips

### As Offense
- CARNIVORE + SHARP VISION + HIGH BODY WEIGHT = unstoppable
- Target weak (undefended) species first
- Build up slowly before striking

### As Defense
- Stack defensive traits on vulnerable species
- HIBERNATION is your safety net
- Mix trait types to stay unpredictable

### General Strategy
- Balance offense and defense
- Diversify your species types
- Watch the food bank and adapt
- Collect food for final scoring

## AI Difficulty

The AI uses sophisticated strategy:
- Evaluates trait synergies
- Adapts to threats
- Makes tactical decisions
- Builds balanced strategies
- Can challenge experienced players

## Modifications & Customization

### Easy Modifications:

**Change AI difficulty:**
Edit `ai.py`, modify scoring multipliers in `AIStrategy.evaluate_trait_value()`

**Add more players:**
Edit `main.py`, add more player names in the `player_names` list

**Adjust deck composition:**
Edit `deck.py`, modify `build_russian_deck()` trait quantities

**Custom rules:**
Edit `game.py` game mechanics in respective phase functions

## Known Limitations

- Text-based interface (not graphical)
- Pair traits (COMMUNICATION, COOPERATION, etc.) handled through base mechanics
- No network multiplayer
- Single-game mode (no tournament)

## Future Enhancements

- Graphical interface
- Expansions support (Time to Fly, Continents, Plantarium)
- Network multiplayer
- Advanced AI with minimax algorithm
- Game statistics and replay system
- Different difficulty levels

## Credits

**Original Game Design:**
- Dmitry Knorre (Moscow State University, Evolutionary Biology)
- Sergey Machin

**Published by:** RightGames RBG

**Implementation:** Python version
**Language:** Python 3.6+

## License

This implementation is a fan-made digital adaptation for educational purposes. 
The original game "Evolution: The Origin of Species" is published by RightGames RBG 
and North Star Games.

## Support & Feedback

For questions, issues, or suggestions about this implementation, 
check the documentation files or review the source code comments.

---

**Enjoy evolving your species! May the most adapted win! 🧬**

=======
# Evolution
Trying to make a working pc version of Evolution (russian version)
>>>>>>> a42aeb6633f76fcced4d837470e726001da0870e
