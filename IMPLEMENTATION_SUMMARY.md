# Evolution: The Origin of Species - Implementation Summary

## Overview
This is a faithful digital implementation of the Russian board game "Evolution: The Origin of Species" created by Dmitry Knorre and Sergey Machin. The game simulates evolutionary adaptation in a competitive ecosystem where players create and evolve species to survive against predators and starvation.

## Core Features Implemented

### 1. Complete Trait System (19 Traits)
All traits from the original game are fully implemented:

**Predatory:**
- **CARNIVORE** (7 copies): Allows attacking other species
- **SHARP VISION**: Enables eating species with CAMOUFLAGE
- **PIRACY**: Steal food from unfed species of other players

**Defensive:**
- **SWIMMING**: Protection against non-swimming carnivores
- **RUNNING**: 50% chance to escape carnivore attacks (dice roll)
- **CAMOUFLAGE**: Hide from carnivores without SHARP VISION
- **HIGH BODY WEIGHT**: Can only be eaten by carnivores with HIGH BODY WEIGHT
- **BURROWING**: Cannot be eaten while fed
- **TAIL LOSS**: Survive attack but sacrifice one trait
- **POISONOUS**: Kill any carnivore that eats this species

**Feeding/Survival:**
- **GRAZING**: Automatically feed from food bank
- **HIBERNATION ABILITY**: Can be marked fed without using food
- **FAT TISSUE**: Store excess food for future rounds
- **COOPERATION** (pair trait): When one allied species gets food, another gets it too
- **COMMUNICATION** (pair trait): Enables food sharing between species
- **SYMBIOSIS** (pair trait): Cannot be eaten while symbiont lives
- **MIMICRY** (pair trait): Choose another species to be eaten instead

**Utility:**
- **SCAVENGER**: Gets food when any species is eaten
- **PARASITE** (negative trait): Applied to opponent species, increases food requirement by 2

### 2. Game Phases

#### Card Play Phase
- Players draw cards equal to: (number of species) + 3
- Interleaved turn system: players take turns playing one card per turn
- Cards can be played as:
  - New species (cards played face down)
  - Traits on existing species (max 3 traits per species)
  - PARASITE on opponent species (requires choosing target player/species)
- Game continues until all players pass consecutively

#### Feeding Phase
- Food bank calculated by dice rolls:
  - 2 players: 1d6 + 2
  - 3 players: 2d6
  - 4 players: 2d6 + 2
- Players take turns feeding their species
- Each species needs 1 food to survive (modified by PARASITE)
- Special traits affect feeding:
  - **GRAZING**: Automatic feed
  - **HIBERNATION**: Marked as fed without using food
  - **FAT TISSUE**: Excess food can be stored
  - **COOPERATION**: Feeding one species feeds another
  - **PIRACY**: Can steal from unfed species

#### Carnivore Attack Phase
- Carnivores attack in player order
- Defense mechanisms:
  - SWIMMING prevents non-swimming carnivores
  - RUNNING triggers dice roll (4-6 = escape)
  - TAIL LOSS saves species but loses a trait
  - BURROWING protects if fed
  - CAMOUFLAGE vs SHARP VISION mechanics
  - POISONOUS kills the attacker
  - SYMBIOSIS protects if partner alive
  - HIGH BODY WEIGHT prevents smaller carnivores
- Each carnivore attacks once per round

#### Extinction Phase
- Unfed species go extinct
- PIRACY activates before extinction
- Surviving species food is collected for scoring
- Game continues until deck runs out

### 3. Scoring System
Based on official rules:
- **+2 points** per surviving species
- **+1 point** per trait on surviving species
- **+1 bonus** for HIGH BODY WEIGHT and CARNIVORE traits
- **+2 points** for PARASITE (special scoring)
- **+1 point** per food collected during the game

### 4. AI Strategy System
The AI uses intelligent decision-making with:

**Trait Evaluation:**
- Scores traits based on:
  - Threat assessment (enemy carnivores present)
  - Current food bank status
  - Synergies with existing traits
  - Strategic value of the trait
- Considers synergy combinations:
  - CARNIVORE synergizes with SHARP VISION, HIGH BODY WEIGHT
  - SWIMMING with SWIMMING (mutual protection)
  - Defensive stacking (CAMOUFLAGE, RUNNING on same species)

**Species Building:**
- Chooses target species based on current traits
- Prefers building specialized species (carnivore, defensive, feeding)
- Avoids weak combinations

**Game Awareness:**
- Reacts to enemy threat level
- Adapts feeding strategy based on food availability
- Makes tactical decisions about PARASITE placement

### 5. Game Loop
- Continues until deck runs out (not fixed rounds)
- Final round triggered when deck has fewer than 3 cards
- Final scores calculated and winner determined

## File Structure

```
EVOLUTION/
├── main.py              # Entry point, game initialization
├── game.py              # Main Game class, game flow control
├── player.py            # Player class, player management
├── species.py           # Species class, species traits and state
├── card.py              # Card class, trait cards
├── deck.py              # Deck class, card management
└── ai.py                # AI strategy and decision making
```

## Key Implementation Details

### Species Class Enhancements
- `has_trait()`: Check for specific traits
- `get_food_requirement()`: Calculate food needed (modified by parasites)
- `can_be_eaten_by()`: Complex defense logic
- `apply_parasite()`: Add parasite effects
- `add_fat_storage()`: FAT TISSUE mechanics

### Game Class Methods
- `calculate_food_bank()`: Proper dice roll mechanics
- `feed_species()`: Handle all feeding trait interactions
- `carnivore_attacks()`: Full defense system
- `extinction_check()`: Handle starvation and PIRACY
- `calculate_scores()`: Accurate scoring

### AI Strategy Class
- `TRAIT_SYNERGIES`: Predefined synergy maps
- `evaluate_trait_value()`: Rate each card
- `choose_target_species()`: Intelligent targeting

## How to Play

1. **Start the game:**
   ```bash
   python main.py
   ```

2. **Card Play Phase:**
   - Enter card number to play (or 'q' to skip)
   - Choose which species to add trait to (or 0 for new species)
   - For PARASITE, choose opponent and their species

3. **Feeding Phase:**
   - Choose which species to feed (in order of need)
   - Some traits feed automatically

4. **Game continues** automatically through attacks and extinction

5. **Final scores** displayed when deck is exhausted

## Differences from Original

The implementation faithfully follows the official rules with these minor simplifications:
- Multiplayer support limited to 2-6 players (expandable)
- Text-based interface (original is physical cards)
- Simplified COMMUNICATION/COOPERATION pair trait UI
- AI makes decisions instantly (no deliberation time)

## Future Enhancement Ideas

1. **Expanded AI:**
   - Minimax algorithm for look-ahead decisions
   - Learning AI that adapts to player strategies
   - Difficulty levels

2. **UI Improvements:**
   - Graphical interface with pygame/tkinter
   - Board state visualization
   - Game history/replay system

3. **Multiplayer:**
   - Network play (online)
   - Tournament mode
   - Statistics tracking

4. **Expansions:**
   - Evolution: Time to Fly
   - Evolution: Continents
   - Evolution: Plantarium

5. **Game Variants:**
   - Fatality scenario
   - Equilibrium scenario
   - Custom rulesets

## Testing

The implementation has been tested for:
- ✅ Correct card distribution (19 traits, 6-7 copies each)
- ✅ Food bank calculation with proper dice rolls
- ✅ All defense mechanics functioning correctly
- ✅ Proper trait synergies
- ✅ Accurate scoring
- ✅ Game ending when deck runs out
- ✅ AI making strategic decisions

## Credits

Game Design: Dmitry Knorre, Sergey Machin
Implementation: [Your Name]
Based on: Evolution: The Origin of Species by RightGames RBG
