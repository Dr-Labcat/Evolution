# Evolution Game - Quick Reference Guide

## Trait Quick Reference

### Predatory Traits
| Trait | Effect | Synergies |
|-------|--------|-----------|
| **CARNIVORE** | Attack other species | SHARP VISION, HIGH BODY WEIGHT |
| **SHARP VISION** | Eat CAMOUFLAGE species | Works with CARNIVORE |
| **PIRACY** | Steal from unfed species | Operates during extinction |

### Defensive Traits
| Trait | Effect | When Active |
|-------|--------|-------------|
| **SWIMMING** | Block non-swimming carnivores | Always |
| **RUNNING** | 50% escape chance (4-6 on d6) | During attack |
| **CAMOUFLAGE** | Hide from non-SHARP VISION carnivores | Always |
| **HIGH BODY WEIGHT** | Block smaller carnivores | Always |
| **BURROWING** | Protection if fed | When fed |
| **TAIL LOSS** | Escape but lose trait | During attack |
| **POISONOUS** | Kill attacking carnivore | During attack |

### Feeding Traits
| Trait | Effect | Usage |
|-------|--------|-------|
| **GRAZING** | Auto-feed from bank | Every feeding turn |
| **HIBERNATION** | Marked fed without food | Can't be used 2 turns in a row |
| **FAT TISSUE** | Store excess food | When fully fed |
| **COOPERATION** | Feed allied species | When one gets food |
| **COMMUNICATION** | Share food between pair | Pair trait mechanic |
| **SCAVENGER** | Get food when species eaten | When extinction happens |

### Special Traits
| Trait | Effect | Counter |
|-------|--------|---------|
| **SYMBIOSIS** | Protect pair from eating | Both must be alive |
| **MIMICRY** | Swap target of attack | Choose different species |
| **PARASITE** | Increase food requirement by 2 | Applied to opponent species |

---

## Game Flow

```
┌─────────────────────────────────────────┐
│      Card Play Phase                    │
│  Players play cards as traits or        │
│  create new species                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Food Bank Determination                │
│  Roll dice: 2p=1d6+2, 3p=2d6,          │
│  4p=2d6+2                              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      Feeding Phase                      │
│  Players take turns feeding species     │
│  (need 1 food + parasites and           │
│other expensive abilities)               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Carnivore Attacks                    │
│  Carnivores attack in player order      │
│  Defenses activate if applicable        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Extinction Check                     │
│  Unfed species are removed              │
│  PIRACY activates                       │
│  Food collected for scoring             │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ Deck empty?  │
        └──┬───────┬───┘
           │       │
          NO      YES
           │       │
           ▼       ▼
       (Next)   (Score &
       (Round)   Winner)
```

---

## Food Requirement Examples

**Base food requirement: 1**

Species with PARASITE:
- 1 PARASITE = 3 food needed
- 2 PARASITES = 5 food needed
- 3 PARASITES = 7 food needed

---

## Scoring Formula

```
Total Points = (2 × surviving species) 
             + (traits on survivors) 
             + (1 bonus per CARNIVORE/HIGH BODY WEIGHT)
             + (2 points per PARASITE)
             + (food collected)
```

---

## Attack Resolution Example

```
Scenario: Herbivore with SWIMMING vs Carnivore without SWIMMING

Attacker: CARNIVORE (no SWIMMING)
Defender: SWIMMING

Result: SWIMMING blocks attack
        Species survives
```

```
Scenario: RUNNING vs Carnivore

Attacker: CARNIVORE
Defender: RUNNING

Resolution: Roll 1d6
           4-6: Escape!
           1-3: Eaten

Result: Depends on dice roll
```

```
Scenario: POISONOUS vs Carnivore

Attacker: CARNIVORE
Defender: POISONOUS

Result: POISONOUS eats carnivore
        Carnivore dies instead
        Species survives
```

---

## Strategic Tips

### For Offense
1. Build CARNIVORE with SHARP VISION + HIGH BODY WEIGHT
2. Create synergies between traits
3. Target weak (undefended) species first

### For Defense
1. Stack defensive traits (SWIMMING + RUNNING + HIGH BODY WEIGHT)
2. Use TAIL LOSS as backup defense
3. BURROWING works better when you can feed regularly

### For Feeding
1. GRAZING gives automatic advantage in low food
2. HIBERNATION is escape valve for bad rounds
3. FAT TISSUE provides multi-round insurance
4. COOPERATION creates feed-through effect

### For Scoring
1. Don't neglect food collection
2. Species count matters (2pts each)
3. Trait diversity builds points (1pt each)
4. Avoid heavy parasite load

---

## Common Card Combinations

**Carnivore Strategy:**
- CARNIVORE + SHARP VISION (eat everything)
- CARNIVORE + HIGH BODY WEIGHT (unstoppable)
- CARNIVORE + SHARP VISION + HIGH BODY WEIGHT (total domination)

**Herbivore Defense:**
- SWIMMING + HIGH BODY WEIGHT (nearly invulnerable)
- CAMOUFLAGE + SHARP VISION (hide + see predators)
- RUNNING + RUNNING + RUNNING (multiple escapes)

**Survival:**
- GRAZING + HIBERNATION (never starve)
- BURROWING + FAT TISSUE (feast or famine proof)

**Chaos Strategy:**
- PARASITE + PIRACY (starve opponents)
- POISON + TAIL LOSS (suicidal defense)

