# Graphical GUI Visual Preview

## What You'll See When You Run the Game

### 1️⃣ Startup Dialog (First)
```
┌─────────────────────────────────┐
│     Player Selection             │
├─────────────────────────────────┤
│                                  │
│  Select number of players:       │
│  2 = You vs AI                   │
│  3 = You, AI, AI                 │
│                                  │
│  [2]  [3]  [Cancel]              │
│                                  │
└─────────────────────────────────┘
```

### 2️⃣ Main Game Window (Then Opens)

```
⚡ ROUND 1 ⚡                              🌾 Food: 12
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────┬──────────────────────────────┐
│                                     │                              │
│  ⚔️ Species Table                   │  👤 Your Turn                │
│                                     │                              │
│  ═══════════════════════════════════│  🎴 Your Hand                │
│  You                                │                              │
│  ═══════════════════════════════════│  ☐ 1. CAMOUFLAGE             │
│                                     │  ☑ 2. GRAZING / HIGH BODY   │
│    Species #1:                      │  ☐ 3. TAIL LOSS             │
│      Body Size: 2                   │  ☐ 4. BURROWING             │
│      Traits: GRAZING, CAMOUFLAGE    │  ☐ 5. COMMUNICATION         │
│      Food Token: 🌾 (2/2)            │                              │
│                                     │  [▶ Play Card]              │
│  ═══════════════════════════════════│  [⊘ Skip Turn]              │
│  AI_1                               │                              │
│  ═══════════════════════════════════│  📢 Messages                 │
│                                     │                              │
│    Species #1:                      │  ✓ Game started!            │
│      Body Size: 1                   │  → AI_1's turn (playing...) │
│      Traits: RUNNING                │  ✓ AI_1 played card         │
│      Food Token: ○ (0/1)             │  → You're playing next      │
│                                     │  ℹ Choose a card to play    │
│                                     │                              │
│                                     │                              │
│    (scroll down for more...)        │  (scroll for more messages) │
│                                     │                              │
└─────────────────────────────────────┴──────────────────────────────┘

Status: Ready
═══════════════════════════════════════════════════════════════════
```

## Color Coding

### Message Colors
- **ℹ Cyan (Info)**: "Game started", "Choose a card", "Round begins"
- **✓ Green (Success)**: "AI played card", "Species fed", "Attack successful"
- **⚠ Yellow (Warning)**: "Low food!", "Final round!", "Species dying"
- **✗ Red (Error)**: "Invalid choice", "Can't feed species", "Error occurred"
- **➜ Magenta (AI)**: "AI thinking...", "AI action complete"

### Data Colors
- **Cyan text**: Your cards, human player info
- **Red text**: AI player info
- **Green**: Available actions
- **Gold**: Food bank when moderate or low

## Layout Sections

### 🔵 Top Bar
```
Round Indicator           Food Bank Status
⚡ ROUND 3 ⚡             🌾 Food: 7
```
- Left: Current round number with lightning bolt icons
- Right: Available food with color indicator
  - Green 🟢 if > 10
  - Gold 🟡 if 5-10  
  - Red 🔴 if < 5

### 🔵 Left Panel (Species Table)
```
═════════════════════════════════════════════
You
═════════════════════════════════════════════

  Species #1:
    Body Size: 2
    Traits: GRAZING, CAMOUFLAGE
    Food Token: 🌾 (2/2)

═════════════════════════════════════════════
AI_1
═════════════════════════════════════════════

  Species #1:
    Body Size: 1
    Traits: RUNNING
    Food Token: ○ (0/1)
```
- Shows all players' current species
- Displays traits and food tokens
- Updates in real-time
- Scrollable for many species

### 🔵 Right Panel - Upper (Hand)
```
🎴 Your Hand

☐ 1. TAIL LOSS
☑ 2. GRAZING / HIGH BODY WEIGHT
☐ 3. HIBERNATION
☐ 4. SYMBIOSIS
☐ 5. SCAVENGER
```
- Numbered list of your cards
- Checkbox shows selection
- Dual-sided cards show both options
- Click to select, then use button

### 🔵 Right Panel - Middle (Buttons)
```
[▶ Play Card]
[⊘ Skip Turn]
```
- **Play Card**: Use selected card
- **Skip Turn**: Pass your turn

### 🔵 Right Panel - Lower (Messages)
```
📢 Messages

✓ Game started!
→ AI_1's turn
✓ AI_1 chose card 2
→ You're up now!
ℹ Select a card to play
⚠ Time limit approaching...
✗ No valid moves
✓ Species created!
→ Feeding phase begins
ℹ Feed species #1?
```
- Scrollable message log
- Color-coded by type
- Newest at bottom
- Shows game flow

### 🔵 Bottom Status Bar
```
Status: Ready (or "Processing...", "Your Turn", "Game Over")
```

## Dynamic Updates During Play

### When You Select a Card
```
✓ Selected: GRAZING
ℹ Choose which species to add trait to:
  1. Species #1 (Body: 2, Traits: CAMOUFLAGE)
  → 2. Species #2 (Body: 1, Traits: RUNNING)
```

### During Feeding Phase
```
→ Feeding phase!
🌾 Food available: 8
ℹ Choose species to feed:
  1. Species #1 (needs 2, have 2)
  → 2. Species #2 (needs 1, have 1)
```

### Carnivore Attack Notification
```
⚠ ALERT: AI_1's carnivore attacks!
→ AI_1 Species #1 (CARNIVORE) attacks You Species #2!
✓ You lost Species #2!
```

### End of Round
```
✓ Round 1 complete!
ℹ Species extinction check...
✓ All species survived!
→ Round 2 starting...
```

## Game Over Screen
```
═══════════════════════════════════════════════════════════════════
🏆 GAME OVER - Final Scores
═══════════════════════════════════════════════════════════════════

You:           42 points
AI_1:          38 points
AI_2:          35 points

🥇 WINNER: You!

Final Statistics:
  Highest species count: 4
  Total food collected: 28
  Best trait combination: GRAZING + COMMUNICATION
  
[Close Window]

═══════════════════════════════════════════════════════════════════
```

## Responsive Design

### Message Auto-Scroll
- Messages automatically scroll to show newest
- No need to manually scroll after each action

### Scrollable Areas
- Species table: Scroll when many species present
- Messages: Scroll to see older events
- Hand: Scroll if window is narrow

### Color Contrast
- Dark background (#0f1419) provides contrast
- Bright text (#00d4ff, #00ff88) easy to read
- No eye strain from bright colors

### Window Stays Responsive
- Even during AI thinking (separate thread)
- You can scroll while AI plays
- Close button always available

## Legend & Icons

| Icon | Meaning |
|------|---------|
| ⚡ | Round indicator |
| 🌾 | Food / Feeding |
| ⚔️ | Species / Combat |
| 🎴 | Cards / Hand |
| 👤 | Player / Turn |
| 📢 | Messages |
| ✓ | Success / Checkmark |
| ⚠ | Warning / Alert |
| ✗ | Error / Negative |
| → | Arrow for direction/next |
| 🥇 | Win / First place |
| 🏆 | Trophy / Achievement |

---

**This is your new Evolution gaming experience - modern, visual, and professional!**
