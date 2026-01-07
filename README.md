# Evolution (Russian Version) — Python Text Implementation

A text-based Python implementation of the Russian board game  
**Evolution: The Origin of Species** by Dmitry Knorre and Sergey Machin.

This project focuses on accurately modeling the **core mechanics, traits, and interactions**
of the game in a terminal-based environment, with a playable AI opponent.

---

## About the Project

**Evolution** is a strategic card game where players create species, assign traits,
and compete for limited food resources. Species must adapt to survive predators,
starvation, and changing ecosystems.

This implementation aims to:
- Recreate the **decision-making depth** of the original game
- Model **trait interactions** clearly and explicitly
- Remain readable, modifiable, and educational

The game is fully playable from the command line and supports human vs AI gameplay.

---

## Current Features

- Text-based gameplay (terminal)
- Human vs AI match
- Full species system (population, body size, food)
- Separate **card play** and **feeding** phases
- Interleaved turns (player → AI → player → AI)
- Trait-based attacks, defenses, and feeding logic
- Automatic cleanup of extinct species
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
