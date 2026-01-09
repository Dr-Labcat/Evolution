# Evolution: The Origin of Species - Python Implementation

A faithful digital implementation of the award-winning board game "Evolution: The Origin of Species". Create species, evolve them with strategic traits, and compete for survival in a dynamic ecosystem.

**[Jump to Quick Start →](#quick-start-guide)**

---

## 🎮 About the Game

**Evolution** is a strategic card game where players compete by creating and evolving species to survive and thrive. Develop traits like CARNIVORE (to hunt), SWIMMING (to escape), POISON (for defense), and combine them strategically to dominate the ecosystem.

**What makes it fun:**
- 19 unique trait cards with deep strategic interactions
- Dynamic food bank system (rolled dice determine available food)
- Complex predator-prey mechanics with multiple defense types
- AI opponents that actually play intelligently
- Replayable with different strategies: pure herbivore, vicious carnivore, or creative trait combinations
- 30-60 minute games

---

# quick start guide

### Installation & Running

**Option 1: From File Explorer (Easiest)**
1. Navigate to the game folder
2. Double-click `play.bat`
3. Game launches in a window with full GUI

**Option 2: From Command Line**
```bash
python main.py
```

**Requirements:**
- Python 3.6+ (uses only standard library)
- Windows/Mac/Linux

### First Game (2 minutes)

1. **Select players**: Choose 2-3 players (you vs AI opponents)
2. **Forfeit a card**: Choose which card to discard for your starting species
3. **Play cards**: Click numbered buttons to play cards during your turn
4. **Feed species**: Choose which species to feed from the food bank
5. **Survive & score**: Keep species alive, collect points

**Goal:** Have the most points when the deck runs out!

---

## 🎯 How to Play

### Game Flow (Each Round)

```
1. CARD PLAY PHASE
   ↓ Players take turns playing cards as traits or creating species
2. FEEDING PHASE  
   ↓ Roll dice for food, choose which species eat
3. CARNIVORE ATTACKS
   ↓ Predators hunt prey, defense traits activate
4. EXTINCTION & SCORING
   ↓ Unfed species die, survivors score points
   (Repeat until deck exhausted)
```

### Your Turn Actions

**During Card Play Phase:**
- **Play a card**: Click a numbered button (1, 2, 3, etc.) showing cards in your hand
- **Add to existing species**: Choose which of your species gets the new trait
- **Create new species**: Choose "Create new" to start a fresh species

**During Feeding Phase:**
- **Choose a species to feed**: Click a button showing your feedable species
- **GRAZING activation**: If your species has this trait, activate it to remove 1 food from bank
- **Skip feeding**: Click "Skip feeding" if no species can or should eat

---

## 🧬 The 19 Traits (Reference)

### Predatory Traits (Hunt Other Species)

| Trait | Effect | Best With |
|-------|--------|-----------|
| **CARNIVORE** | Attack and eat other species | HIGH BODY WEIGHT, SHARP VISION |
| **SHARP VISION** | Hunt CAMOUFLAGE species that normally hide | Any CARNIVORE |
| **PIRACY** | Steal food from unfed species during extinction | CARNIVORE for synergy |

### Defensive Traits (Block Attacks)

| Trait | Blocks | Notes |
|-------|--------|-------|
| **SWIMMING** | Non-swimming carnivores | Always active |
| **RUNNING** | Any attack | 50% escape chance (roll 4-6 on d6) |
| **CAMOUFLAGE** | Non-SHARP VISION carnivores | Always active |
| **HIGH BODY WEIGHT** | Smaller carnivores (must have higher body size) | Increases food need |
| **BURROWING** | Carnivore attacks | Only works if species is fed |
| **TAIL LOSS** | Attack | Escape but lose this trait |
| **POISONOUS** | Carnivore | Kill the attacker outright |

### Feeding & Synergy Traits

| Trait | Effect | Usage |
|-------|--------|-------|
| **GRAZING** | Auto-feed from bank (remove 1 food, species gets fed) | Activates each feeding turn |
| **HIBERNATION** | Mark species as fed without using food | Can't use 2 turns in a row |
| **FAT TISSUE** | Store extra food when fully fed | Use when food bank is high |
| **COOPERATION** | Share food: when one species gets food, allied species also get food | Triggered together |
| **SCAVENGER** | Get food when another species is eaten | During extinction phase |

### Special/Complex Traits

| Trait | Effect | Strategy |
|-------|--------|----------|
| **SYMBIOSIS** | Pair of species protect each other from being eaten | Create dangerous pairs |
| **MIMICRY** | Redirect carnivore attack to different target species | Defensive trick |
| **PARASITE** | Add to opponent's species, increases their food requirement by 2 | Sabotage enemy |

---

## 💡 Strategy Tips

### Beginner Strategy
- **Herbivore path**: Build a single large peaceful species with GRAZING - safe and steady
- **Simple carnivore**: CARNIVORE + HIGH BODY WEIGHT = hunt smaller species easily
- **Multiple small species**: Many 1-size species are harder to kill individually

### Intermediate Strategy
- **Trait synergies**: SWIMMING + CARNIVORE hunts safely; COMMUNICATION pairs share food
- **Food efficiency**: GRAZING or HIBERNATION reduce your food needs
- **Hybrid species**: One carnivore + multiple herbivores creates balanced ecosystem

### Advanced Strategy
- **SYMBIOSIS pairs**: Two species protecting each other create dangerous combinations
- **PARASITE sabotage**: Cripple the leader's species during feeding phase
- **Trait combos**: COOPERATION + FAT TISSUE = food storage engine
- **Timing**: Know when to attack vs. when to grow defensively

---

## 📊 Scoring

**Points awarded for:**
- **Each surviving species**: 2 points
- **Each trait on a survivor**: 1 point per trait
- **Each food token collected**: 1 point

**Example:** A species with body size 2, 2 traits, and 1 food = 2 (species) + 2 (traits) + 1 (food) = **5 points**

---

## 🏗️ Project Structure

```
EVOLUTION/
├── main.py              # Game entry point + launcher
├── play.bat             # Click to play (Windows)
├── assets/
│   ├── game.py          # Core game logic & flow
│   ├── player.py        # Player management
│   ├── species.py       # Species traits & mechanics
│   ├── card.py          # Card/trait definitions
│   ├── deck.py          # Deck management
│   ├── ai.py            # AI strategy
│   ├── gui_window.py    # Graphical interface (tkinter)
│   └── gui_bridge.py    # Game ↔ GUI communication
└── README.md            # This file
```

---

## 🖥️ GUI Controls

- **Action buttons**: Click numbered buttons (1, 2, 3, etc.) to make choices
- **Species table** (left): Shows all players' species with traits, food status, and fat storage
- **Your hand** (right top): Lists cards you can play
- **Actions panel** (right middle): Shows available choices with numbered buttons
- **Message log** (right bottom): Game events and descriptions
- **Status bar**: Current round and food bank amount

---

## 🐛 Known Limitations

- AI doesn't use PARASITES strategically
- Some complex trait combinations may have edge cases
- Text widget displays basic information (emojis may not show depending on system font)

---

## 🔧 Technical Details

**Architecture:**
- Game logic completely decoupled from GUI
- Runs game in background thread to keep UI responsive
- All user input through GUI buttons (no terminal required)
- Fallback to terminal mode if no GUI window detected

**Dependencies:**
- Python 3.6+ standard library only (tkinter for GUI)
- No external packages required

---

## 📝 License & Credits

Based on "Evolution: The Origin of Species" by Dmitry Knorre and Sergey Machin.

---

## ❓ FAQ

**Q: Can I play with more than 3 players?**  
A: The code supports 2-3 players (2 vs AI, or 3 with AI). Can be extended but balance testing needed.

**Q: Why can't I run `main.py` by double-clicking it?**  
A: Windows needs the virtual environment activated. Use `play.bat` instead!

**Q: How do I beat the AI?**  
A: The AI uses solid strategy but isn't perfect. Try: multiple small species, GRAZING + large herbivores, or PARASITE sabotage.

**Q: What's the longest game?**  
A: With lucky dice rolls and many species, 60 minutes. Most games finish in 30-40 minutes.

---

**Ready to evolve? Double-click `play.bat` or run `python main.py`!**

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
