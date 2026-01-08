# Graphical GUI Quick Start

## Launch the Game

```bash
python main.py
```

## Startup Dialog

A dialog appears asking you to select:
- **2 Players** = You vs 1 AI
- **3 Players** = You vs 2 AIs

Select and click OK.

## The Game Window

### Top Bar
- **Left**: Round number (⚡ ROUND 1 ⚡)
- **Right**: Food bank with color indicator (🌾 Food: 12)

### Left Panel: Species Table
Shows all players' species in a scrollable area:
```
==============================================
You
==============================================

  Species #1:
    Body Size: 2
    Traits: GRAZING, CAMOUFLAGE
    Food Token: 🌾 (1/2)
```

### Right Panel: Your Control Center

**👤 Your Turn**
- Shows whose turn it is

**🎴 Your Hand**
- List of cards you can play
- Click to select a card
- Dual-sided cards show both options (e.g., "PARASITE / CARNIVORE")

**[Play Card] and [Skip Turn] Buttons**
- Play the selected card
- Skip your turn if you prefer

**📢 Messages**
- Scrollable log of all game events
- Color-coded:
  - 🔵 Cyan = Information
  - 🟢 Green = Success
  - 🔴 Red = Error
  - 🟡 Yellow = Warning

## Color Meanings

| Color | Meaning |
|-------|---------|
| 🔵 Cyan | Your actions / human player |
| 🔴 Red | AI actions / danger |
| 🟣 Magenta | Special/accent |
| 🟢 Green | Success/positive |
| 🟡 Gold | Warning/attention |

## Game Phases

The game automatically cycles through:

1. **Card Play Phase**: Choose which card to play (or skip)
2. **Feeding Phase**: Choose which species to feed
3. **Carnivore Attacks**: Automatic (AI controlled)
4. **Extinction Check**: Automatic (removes unfed species)

## Window Controls

- **Close Button (X)**: Ends the game and closes the window
- **Scroll Bars**: Scroll through species table or messages
- **Listbox Selection**: Click a card in your hand to select it

## Food Bank Colors

| Color | Condition |
|-------|-----------|
| 🟢 Green | >10 food (abundant) |
| 🟡 Yellow | 5-10 food (moderate) |
| 🔴 Red | <5 food (scarce) |

## Common Actions

### Play a Card
1. Card appears in your hand list
2. Click the card to select it
3. Click [Play Card] button
4. Follow any prompts (e.g., select target species)

### Feed a Species
During feeding phase:
1. Available species listed in messages
2. Messages prompt you to choose
3. Select and confirm

### View Species Details
- Species Table shows all active species
- Updates in real-time as game progresses

## Status Bar

Bottom of window shows:
- Current game status
- Ready/Processing indicators

## Tips for Better Experience

✓ Keep the window visible and at a comfortable size  
✓ Scroll the messages area for full event history  
✓ Check the species table before making decisions  
✓ Review your hand before your turn starts  
✗ Avoid closing the window mid-game (may cause errors)  

## Troubleshooting

**Window is frozen?**
- The game is processing AI turns
- Wait a few seconds for the game to respond

**Unicode characters look weird?**
- Your terminal encoding may need adjustment
- The GUI should handle them correctly

**Cards not showing up?**
- Scroll the hand listbox down
- Window may be too narrow (try maximizing)

**Game won't start?**
- Check you have Python 3.12+ installed
- Ensure all assets files are present
- Try running from the EVOLUTION directory

---

**Need Help?** Check the full documentation in GUI_README.md
