# How to Play Evolution — Complete Guide

Evolution is played over several rounds. Each round has three phases: **Card Play**, **Feeding**, and **Extinction**. The game ends when the deck runs low, then scores are calculated.

## Starting the Game

```bash
python main.py
```

You'll be asked to enter your name (or accept "You"). The game will then:
1. Deal you 5 trait cards
2. Ask you to discard one card to create your first species
3. Start Round 1

## Phase 1: Card Play

In this phase, players take turns (you go first, then the AI, back and forth) to play one card from their hand.

**On your turn, you can:**
- **Play a card on an existing species** (add a trait)
- **Play a card as a new species** (use it as the base; discard a trait from your hand later)
- **Press 'q' to pass** (skip this turn; other players continue)

**Special case — PARASITE:**
If you play a PARASITE card, you must choose an opponent and one of their species to infect. The parasite adds +2 to that species' food requirement, making it harder to feed.

**Traits per species:**
Each species can have up to 3 traits. Once full, you must create a new species to add more traits.

**Passing:**
Once you pass, you sit out the rest of Card Play; other players continue until everyone has passed.

## Phase 2: Feeding

After everyone has passed, the food bank is rolled:
- **2 players**: 1d6 + 2
- **3 players**: 2d6
- **4 players**: 2d6 + 2
- **5 players**: 3d6 + 2

Players then take turns choosing one action per turn, in a round-robin fashion:

### Your Three Action Options

#### Option 1: Feed from the Food Bank
Choose an unfed species and give it 1 food from the bank (up to its food requirement).
- If a species is already fed, the food is automatically stored as FAT TISSUE (if it has the trait).
- If a species has COOPERATION, its neighbor also gets 1 food automatically.

#### Option 2: Use Animal Abilities
Activate a special trait on one of your species:
- **GRAZING**: Remove 1 from the food bank without feeding (once per species per round)
- **HIBERNATION**: Mark a species as "fed" without using food (counts as hibernating; resets next round)
- **CONVERT FAT**: Spend stored FAT TISSUE tokens to feed your species

#### Option 3: Attack with a Carnivore (Your Turn Only)
If you own a CARNIVORE that hasn't attacked this round, you can attack an opponent's species:

1. **Choose your carnivore**
2. **Choose a target** from opponent species (the game shows you what defenses apply)
3. **Resolve the attack**:
   - If target has SWIMMING and your carnivore doesn't, blocked (species survives)
   - If target has CAMOUFLAGE and your attacker lacks SHARP VISION, blocked
   - If target has HIGH BODY WEIGHT and your attacker is smaller, blocked
   - If target has BURROWING and is fed, blocked
   - If target has RUNNING, roll a die: 4–6 = escape
   - If target has TAIL LOSS, it can discard a trait to survive
   - If target has POISONOUS, your carnivore dies instead
4. **Success**: Target is removed; your carnivore gains 2 food (goes to FAT if already fed)

**Mandatory Feeding Rule:**
If you have unfed species or unfilled FAT TISSUE slots and the food bank has food, you must take an action. You cannot skip indefinitely while obligations exist.

### During Feeding, Opponents May React
- If a species receives red food (from the bank or GRAZING), an opponent with PIRACY can steal 1 from it
- When a species is eaten, all SCAVENGER species gain 1 food (even on opponent turns)

### End of Feeding
Once all players pass consecutively, move to Extinction.

## Phase 3: Extinction & Scoring

Species that didn't get enough food may die:

1. **Check feeding**: Unfed species (with no FAT to convert) face extinction
2. **Protections apply**:
   - FAT TISSUE: Automatically consumed to meet the food requirement
   - SYMBIOSIS: If paired correctly, a species survives even if unfed (partner must be alive and larger)
   - BURROWING: Already applied during attacks; not checked again here
3. **Remove extinct species**
4. **Collect food**: Surviving species contribute their food tokens to your score pool

Once extinction is done, check if the deck is depleted. If yes, proceed to final scoring. Otherwise, start a new round.

## End Game & Scoring

When the deck runs low (fewer than 3 cards), the current round is the last.

Final scoring:
- **+2 points** per surviving species
- **+1 point** per trait on each surviving species
- **+1 bonus** for CARNIVORE and HIGH BODY WEIGHT on survivors
- **+2 points** per PARASITE on surviving species (penalties and rewards!)
- **+1 point** per food token in your collected pool

The player with the highest score wins.

## Example Game Round

### Card Play
```
Round 1 starts. You have 5 cards: SWIMMING, CARNIVORE, FAT TISSUE, GRAZING, PARASITE

--- You's turn ---
You play SWIMMING as a new species. You're asked to discard a card to form the species.
You discard PARASITE, so your species is created with SWIMMING.

--- AI_1's turn ---
AI plays a card on their species.

--- You's turn ---
You play CARNIVORE on your SWIMMING species.
Now you have one species: [SWIMMING, CARNIVORE].

--- AI_1's turn ---
AI plays another card and passes.

--- You's turn ---
You play FAT TISSUE on your SWIMMING species.
Now your species is at max traits (3): [SWIMMING, CARNIVORE, FAT TISSUE].
You pass.

All players have passed, so card play ends.
```

### Feeding
```
Food bank: 6

--- You's feeding turn ---
Your species is unfed (needs 1 food + 1 for CARNIVORE = 2 total).
You have 3 options:
  1: Feed from the food bank (take 1 food)
  2: Use abilities (no options available yet)
  3: Attack with your CARNIVORE

You choose Option 1: Feed your species.
Your species gets 1 food. Food bank now: 5. Your species: 1/2 fed.

--- AI_1's feeding turn ---
AI feeds their species.
Food bank now: 4.

--- You's feeding turn ---
Your species still needs 1 more food.
You choose Option 1 again: Feed your species.
Your species gets 1 food. Food bank now: 3. Your species: 2/2 fed (fully fed).

--- AI_1's feeding turn ---
AI tries to feed, but then passes.

--- You's feeding turn ---
Your species is fully fed. If you take food now, it auto-stores to FAT TISSUE.
You choose Option 3: Attack with your CARNIVORE.

You target AI_1's species. It has no special defense.
Attack succeeds: AI_1's species is removed. Your CARNIVORE gains 2 food.
Since your species is already fed, the 2 food is auto-stored as FAT (1 fat token used of 1 available).

--- AI_1's feeding turn ---
AI has no unfed species, so passes.

--- You's feeding turn ---
You pass (nothing more to do).

Final: All pass. Feeding ends.
```

### Extinction
```
No unfed species remain, so no extinctions.
Your species survives with 1 food token (collected for final scoring).

Deck check: Plenty of cards remain, so Round 1 is complete.
```

## Strategy Tips

### Early Game (Rounds 1–2)
- **Build diversity**: Create multiple species to spread risk
- **Don't overdraft the food bank**: Leave some food for others; long-term reputation matters
- **Defensive traits first**: Species without defense often die

### Mid Game (Rounds 3–5)
- **Notice opponents' builds**: Is someone going for carnivores? Get SWIMMING or RUNNING
- **Chain feeding engines**: COOPERATION + COMMUNICATION can feed many species from one action
- **Fat up for scarcity**: If the food bank has been low, store FAT for lean rounds

### Late Game (Final Rounds)
- **Maximize survivors**: Each species is worth 2 points; preservation beats offense
- **Collect food**: Food is scarce and worth points
- **Avoid new species unless necessary**: Unfinished species often go extinct

## Common Questions

**Q: Can I attack my own species?**  
No, CARNIVORE only targets opponents' species.

**Q: Does FAT TISSUE auto-apply?**  
Yes. If a species is fed and gets food, it automatically goes to FAT (if it has the trait and room).

**Q: Can PARASITE be used offensively?**  
Yes. Playing PARASITE on an opponent's species is often a powerful move.

**Q: What if I can't feed all my species?**  
Some will go extinct. It's a core mechanic: hard choices about which species survive.

**Q: Can I pass during feeding?**  
Yes, but only if you have no unfed species or unfilled FAT (or the food bank is empty). Otherwise, you must act.

## For More Details

See `QUICK_REFERENCE.md` for a trait-by-trait breakdown, attack resolution flowcharts, and scoring examples.
