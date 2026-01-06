# How to Play Evolution

## Starting the Game

```bash
python main.py
```

The game will display:
- Current round number
- Whose turn it is
- Available actions
- Game state (species, food bank, etc.)

## Card Play Phase

### Your Turn Prompt:
```
--- You's turn ---
Your species:
1: Body-size:1 Food:0/1 Traits:[]
Your hand:
1: SWIMMING
2: CARNIVORE
3: FAT TISSUE
Play card? Enter card number or 'q' to skip:
```

### What to Do:
1. **Enter a number (1-3 in above example)** to play that card
2. **Enter 'q'** to skip your turn and let other players play

### After Playing a Card:

You'll see:
```
Add to species (1-1) or create new (0)? 
```

**Options:**
- **Enter 0**: Create a brand new species with this card
- **Enter 1**: Add the trait to species #1 (if it has space)

### Special Case - PARASITE:

If you play PARASITE:
```
Which opponent species to infect with PARASITE?
1: AI_1
Choose opponent (or 'q' to cancel):
```

1. Choose the opponent number
2. Choose which of their species to infect

---

## Feeding Phase

### Your Turn:
```
--- You's feeding turn ---
Food bank: 4
Your unfed species:
1: Body-size:1 Food:0/1 Traits:[SWIMMING]
2: Body-size:1 Food:0/2 Traits:[PARASITE]
Feed species 1-2 (or 'q' to skip):
```

**What to Do:**
- Enter **1 or 2** to feed that species
- Enter **'q'** to skip feeding (species might go extinct!)

### Food Requirements:
- **Base: 1 food** (to survive one round)
- **+2 per PARASITE** (so 2 parasites = 5 food needed!)
- **HIBERNATION**: Can be marked fed without using food

### Special Traits in Feeding:
- **GRAZING**: Automatically gets food
- **FAT TISSUE**: Can store excess food
- **COOPERATION**: Feeding one species feeds its partner
- **HIBERNATION**: Can skip a turn

---

## Carnivore Attacks (Automatic)

Watch the game automatically resolve attacks:

```
=== Carnivore Attacks ===
AI_1's CARNIVORE attacked You's SWIMMING species!
Protected by SWIMMING
AI_1's CARNIVORE attacked You's second species!
AI_1's CARNIVORE ate You's species!
```

### Defense Mechanics:
- **SWIMMING** blocks non-swimming carnivores
- **RUNNING** has 50% chance (4-6 on dice roll)
- **CAMOUFLAGE** hides unless carnivore has SHARP VISION
- **HIGH BODY WEIGHT** blocks smaller carnivores
- **BURROWING** protects if fed
- **TAIL LOSS** saves species but loses a trait
- **POISONOUS** kills the carnivore!

---

## Extinction Phase (Automatic)

The game automatically:
1. Removes any unfed species (they starve)
2. Activates PIRACY (steals from unfed species)
3. Collects food for scoring
4. Checks if deck is empty

```
=== Extinction Check ===
You's species with GRAZING survived! (Food: 3)
You's unfed species went extinct!
```

---

## End of Game

When the deck runs out:

```
==================================================
=== GAME OVER ===
==================================================

Final Scores:
AI_1: 24 points
You: 31 points

🎉 You wins with 31 points!
```

### Score Breakdown:
- **+2 points** per surviving species
- **+1 point** per trait on survivors
- **+1 bonus** for CARNIVORE and HIGH BODY WEIGHT traits
- **+1 point** per food collected during game

---

## Example Game Walkthrough

### Round 1 - Card Play

```
--- You's turn ---
Your species:
1: Body-size:1 Food:0/1 Traits:[]
Your hand:
1: SWIMMING
2: CARNIVORE
3: GRAZING
Play card? Enter card number or 'q' to skip: 1

Add to species (1-1) or create new (0)? 0
✓ Created new species (card SWIMMING used as species card)
```

Now you have 2 species.

```
--- You's turn (continued) ---
Your hand:
1: CARNIVORE
2: GRAZING
Play card? Enter card number or 'q' to skip: 1

Add to species (1-2) or create new (0)? 1
✓ Added CARNIVORE to species 1
```

You've built a CARNIVORE!

### Round 1 - Feeding Phase

```
--- You's feeding turn ---
Food bank: 5
Your unfed species:
1: Body-size:1 Food:0/1 Traits:[SWIMMING, CARNIVORE]
2: Body-size:1 Food:0/1 Traits:[]
Feed species 1-2 (or 'q' to skip): 1

✓ Fed species 1 (needs 1 total)
```

Your CARNIVORE is now fed and can attack!

### Round 1 - Carnivore Attacks

```
=== Carnivore Attacks ===
You's CARNIVORE attacked AI_1's species!
You's CARNIVORE ate AI_1's species!
```

You destroyed an enemy!

### Round 1 - Extinction

```
=== Extinction Check ===
You's species survived! (Food: 1)
You's unfed species went extinct due to starvation!
```

One species survives, one died from starvation.

---

## Tips for Better Play

### Early Game (First 2 Rounds)
1. Build diverse species first
2. Don't be too aggressive immediately
3. Get a mix of traits to adapt later

### Mid Game (Rounds 3-5)
1. Notice what opponents are building
2. Start defensive builds if they have carnivores
3. Build feeding engines for scarce food rounds

### Late Game (When Deck Gets Low)
1. Go for maximum survival
2. Make species as hard to kill as possible
3. Collect food for scoring

### Always Remember
- **Food matters!** It's worth points at the end
- **Diversity matters!** More species = more points
- **Traits matter!** Stacked traits are powerful
- **Don't overspecialize!** A mix of types is better

---

## Troubleshooting

**"Game doesn't progress when I press q"**
- Make sure you type 'q' and press Enter
- 'q' skips your turn and ends that phase when all players pass

**"Can't add trait to species"**
- Each species can only have 3 traits max
- Create a new species instead

**"Species keeps going extinct"**
- Not getting enough food from the bank
- Try using HIBERNATION or GRAZING traits
- Make sure parasite load isn't too high

**"How do I attack?"**
- You need CARNIVORE trait on a species
- Attacks happen automatically during Carnivore Attack Phase
- You don't control them - they happen in player order

**"Food bank is too low"**
- That's the luck of the dice roll!
- HIBERNATION and PIRACY help during low food
- GRAZING ensures at least some food

