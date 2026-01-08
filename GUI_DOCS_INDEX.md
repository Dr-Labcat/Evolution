# Russian Evolution - GUI Documentation Index

Welcome! Your Russian Evolution card game now has a professional graphical interface. This index helps you find the right documentation.

## 📚 Documentation Files

### For Players/Getting Started
- **[GUI_QUICKSTART.md](GUI_QUICKSTART.md)** - 5-minute quick start guide
  - How to launch the game
  - Startup dialog walkthrough
  - Window controls and interface explanation
  - Common actions (play card, feed species)
  - Troubleshooting tips

- **[GUI_PREVIEW.md](GUI_PREVIEW.md)** - Visual walkthrough
  - Screenshots of what you'll see
  - Color coding explained
  - Layout sections detailed
  - Dynamic updates examples
  - Message log examples
  - Icons and legend

### For Technical Details
- **[GUI_README.md](GUI_README.md)** - Comprehensive technical documentation
  - Feature overview
  - Architecture and design
  - Module descriptions
  - Game flow with GUI
  - Color scheme specifications
  - Future enhancement ideas

- **[GUI_IMPLEMENTATION.md](GUI_IMPLEMENTATION.md)** - Implementation details
  - Files created and modified
  - Design decisions
  - Component breakdown
  - Threading model
  - Testing results
  - Known limitations

### Original Documentation (Still Valid!)
- **[README.md](README.md)** - Original game overview
- **[HOW_TO_PLAY.md](HOW_TO_PLAY.md)** - Game rules and mechanics
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Card reference
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Original implementation notes

## 🎮 Quick Start

```bash
# Run the game
python main.py

# Select 2 or 3 players when prompted
# Game window opens automatically
# Play your turns by selecting cards
# Watch the AI play
# Enjoy the game!
```

## 📋 File Structure

```
EVOLUTION/
├── main.py                          # Game launcher (uses GUI)
├── assets/
│   ├── gui_window.py               # NEW: Graphical GUI
│   ├── gui_bridge.py               # NEW: GUI-Game connector
│   ├── gui.py                      # OLD: Terminal GUI (fallback)
│   ├── game.py                     # Game logic (updated)
│   ├── player.py                   # Player management
│   ├── species.py                  # Species mechanics
│   ├── card.py                     # Card data
│   ├── deck.py                     # Deck management
│   └── ai.py                       # AI strategy
├── GUI_QUICKSTART.md               # This file's sister docs
├── GUI_README.md
├── GUI_PREVIEW.md
├── GUI_IMPLEMENTATION.md
└── [Other docs...]
```

## 🎯 What to Read

### "I just want to play!"
→ Read **GUI_QUICKSTART.md** (10 minutes)

### "I want to see what it looks like"
→ Read **GUI_PREVIEW.md** (5 minutes)

### "I want to understand how it works"
→ Read **GUI_README.md** (15 minutes)

### "I want technical/code details"
→ Read **GUI_IMPLEMENTATION.md** (10 minutes)

### "I need to modify/extend the GUI"
→ Read all above + check **assets/gui_window.py** code (30 minutes)

### "I want to understand the game mechanics"
→ Read **HOW_TO_PLAY.md** (20 minutes)

## 🔑 Key Features at a Glance

| Feature | Description |
|---------|-------------|
| 🪟 **Window** | 1400x900 graphical window |
| 🎨 **Theme** | Professional dark theme |
| 📊 **Display** | Real-time species, hand, food, messages |
| 🎴 **Cards** | Numbered selection with dual-side support |
| 📢 **Messages** | Color-coded game event log |
| 🧵 **Threading** | Game runs in background thread |
| ↔️ **Dual Mode** | Works with GUI or terminal |
| 🎯 **Responsive** | Window stays interactive |

## 🎨 Color Quick Reference

```
👤 Cyan (#00d4ff)      = Your player / Actions
🤖 Red (#ff0000)       = AI player / Danger
✓ Green (#00ff88)      = Success / Positive
⚠️ Yellow (#ffd700)    = Warning / Attention
ℹ️ Blue (#0099ff)      = Information
🎲 Magenta            = Special / Accent
```

## 🚀 Getting Started (3 Steps)

1. **Open Terminal/PowerShell**
   ```bash
   cd c:\Users\kzinz\Documents\Informatica\EVOLUTION
   ```

2. **Run the Game**
   ```bash
   python main.py
   ```

3. **Select Players**
   - Dialog appears asking for 2 or 3 players
   - Click your choice
   - Game window opens!

## ❓ Common Questions

**Q: How do I play a card?**
A: Select it in the hand list, click "Play Card"

**Q: What do the colors mean?**
A: Cyan = you, Red = AI. See GUI_PREVIEW.md

**Q: Can I resize the window?**
A: Yes, but layout works best at 1400x900

**Q: What if the window freezes?**
A: That's normal during AI turns. Wait 2-3 seconds.

**Q: Can I play without the GUI?**
A: Not in current version, but it falls back to terminal if needed

**Q: Where are the game rules?**
A: See HOW_TO_PLAY.md

**Q: How do I customize colors?**
A: Edit assets/gui_window.py and search for hex colors

## 🔧 For Developers

### To Understand the Code
1. Read **GUI_IMPLEMENTATION.md** (architecture overview)
2. Check **assets/gui_window.py** (GUI code - 230 lines)
3. Check **assets/gui_bridge.py** (bridge functions - 80 lines)
4. Check **assets/game.py** (updated Game class)

### Key Classes
- `GameWindow` (gui_window.py) - Main GUI interface
- `Game` (game.py) - Game logic with GUI support

### Key Methods
- `GameWindow.update_round()` - Update round display
- `GameWindow.update_food()` - Update food display
- `GameWindow.update_species()` - Update species table
- `GameWindow.update_hand()` - Update card hand
- `GameWindow.add_message()` - Post message to log
- `Game.update_gui_display()` - Sync game state to GUI

### To Modify the GUI
1. Edit colors in `GameWindow.__init__()` style configuration
2. Adjust layout in `GameWindow.setup_ui()`
3. Add new display elements by extending GUI class
4. Update game logic calls in `Game` class

## 📞 Support & Resources

### Game Rules Questions
- See: **HOW_TO_PLAY.md**
- See: **QUICK_REFERENCE.md** for card list

### GUI Questions
- See: **GUI_QUICKSTART.md** for user guide
- See: **GUI_PREVIEW.md** for visual walkthrough

### Technical Questions
- See: **GUI_README.md** for features and architecture
- See: **GUI_IMPLEMENTATION.md** for technical details

### Bugs/Issues
- Check: **GUI_QUICKSTART.md** troubleshooting section
- Check: Window is actually responsive (wait a few seconds)
- Check: All files in assets/ are present

## 🎓 Learning Path

**Beginner** (Just Play)
- GUI_QUICKSTART.md (10 min)
- Start playing!

**Intermediate** (Understand It)
- GUI_PREVIEW.md (5 min)
- GUI_README.md (15 min)
- Read HOW_TO_PLAY.md (20 min)
- Play several games!

**Advanced** (Modify/Extend)
- All above (50 min)
- GUI_IMPLEMENTATION.md (10 min)
- Read source code (30 min)
- Modify and test (variable)

## 📦 What's New?

Compared to terminal version:
- ✨ Professional graphical window
- ✨ Real-time display updates
- ✨ Better information layout
- ✨ Color-coded messages
- ✨ Scrollable content areas
- ✨ Modern dark theme
- ✨ Responsive UI (separate game thread)
- ✨ Cleaner player experience

What stayed the same:
- ✓ All game rules intact
- ✓ Same card deck (84 cards)
- ✓ Same game mechanics
- ✓ Same AI strategy
- ✓ All original features

## 📝 Document Information

- **Last Updated**: January 2026
- **Version**: 2.0 (Graphical GUI)
- **Python**: 3.12.6+
- **Library**: tkinter (built-in)
- **Status**: ✅ Production Ready

---

## Next Steps

1. **Start Playing**: Run `python main.py`
2. **Check QUICKSTART**: Read GUI_QUICKSTART.md for help
3. **Have Fun**: Enjoy your new graphical Evolution!

Questions? Each documentation file covers specific topics. Start with the one matching your need above.

**Happy Gaming! 🎮🃏**
