# Evolution — Python Text Implementation

**A playable, expressive, terminal-based implementation of the Russian edition of Evolution.**

Evolution is a strategic card game where players design and adapt species to survive in a competitive ecosystem. This project brings that experience to the command line, with a working AI opponent and all core mechanics faithfully implemented.

## About This Project

This implementation focuses on:
- **Playability**: Human vs AI matches that actually feel like the board game
- **Clarity**: Trait logic and interactions are explicit and readable
- **Extensibility**: Easy to add new traits, modify AI, or add test coverage

It's designed for players who want to practice or play offline, and for developers who want to understand Evolution's decision-making framework through code.

## What You Can Do

- Play full games (2–5 players, one human + AI opponents)
- Create species with custom trait combinations
- Experience realistic feeding pressure and trade-offs
- Watch your species evolve (or go extinct)
- Score and see a final winner

## Key Mechanics

- **Card Play**: Build species by playing trait cards or creating new ones
- **Feeding Phase**: Take turns feeding from a shared food bank, with integrated carnivore attacks
- **Extinction**: Unprepared species starve; others survive and score points
- **Traits**: 19 traits with different roles (predatory, defensive, feeding-focused, special)
- **Fat Tissue Storage**: Bank food for lean rounds
- **Cooperation & Chains**: Build feeding engines that support multiple species

## Quick Start

```bash
python main.py
```

You'll be prompted to choose a card to start your first species, then play begins.

## Project Layout

```
assets/
  game.py          — main game loop and phase management
  species.py       — species state and trait interactions
  player.py        — player data and card play
  deck.py          — 84-card Russian deck
  card.py          — card representation
  ai.py            — basic AI strategies

scripts/           — optional utilities (developer-focused)
README.md          — this file
HOW_TO_PLAY.md     — gameplay walkthrough and examples
QUICK_REFERENCE.md — trait reference and rules summary
```

## How It Works (At a High Level)

1. **Round Setup**: Players draw cards, food bank is rolled
2. **Card Play**: Players take turns adding traits or creating species
3. **Feeding**: Players choose actions: feed, use abilities, or attack
4. **Extinction**: Unfed species are removed (or protected by special traits)
5. **Scoring**: Points awarded for surviving species, traits, and collected food
6. **Game End**: When the deck runs low, final scores are calculated

## For Players

If you're new to Evolution, start with `HOW_TO_PLAY.md` for a walkthrough. `QUICK_REFERENCE.md` has a trait table and examples.

## For Developers

The code is intentionally simple:
- No external dependencies (Python 3.10+)
- Trait logic is localized and easy to inspect
- Game phases are separate methods
- AI decisions are rule-based and transparent

To extend:
- Add new traits by modifying `deck.py` and handling them in `species.py` or `game.py`
- Improve AI by editing strategy methods in `ai.py`
- Add unit tests to verify trait interactions

## Contributing

Small, focused changes are welcome. Please:
- Keep logic clear and readable
- Add test cases for new traits or mechanics
- Update documentation if behavior changes

## References

- Evolution (board game) — originally designed by Dmitry Knorre and Sergey Machin
- This implementation interprets the Russian rules as provided
- Endgame scoring

---

## Implemented Traits

The game includes **19 trait cards**, covering offensive, defensive, and feeding mechanics:

### Predatory / Aggressive
- CARNIVORE  
- SHARP VISION  
- PIRACY  

### Defensive
- SWIMMING  
- RUNNING  
- CAMOUFLAGE  
- HIGH BODY WEIGHT  
- BURROWING  
- TAIL LOSS  
- POISONOUS  

### Feeding & Support
- GRAZING  
- HIBERNATION  
- FAT TISSUE  
- COOPERATION  
- COMMUNICATION  
- SCAVENGER  

### Special
- SYMBIOSIS  
- MIMICRY  
- PARASITE  

Trait interactions are explicitly handled in code and designed to be easy to inspect
or extend.

---

## How to Run

### Requirements
- Python 3.10+ recommended  
- No external dependencies (standard library only)

### Start the Game
```bash
python main.py
