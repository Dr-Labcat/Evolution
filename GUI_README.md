# Russian Evolution - Graphical GUI Version

## Overview

Your Russian Evolution card game now features a professional graphical GUI built with **tkinter**! Instead of a terminal-based text interface, you now get a proper pop-out window with a modern dark theme, real-time game updates, and intuitive card displays.

## Features

### 🎮 Modern Graphical Interface
- **Dark Theme**: Professional #0f1419 background with vibrant cyan, magenta, and green accents
- **Real-time Updates**: Species table, hand display, food bank, and round counter all update dynamically
- **Responsive Design**: 1400x900 window with properly organized game information

### 🎯 Game Display Elements
- **Species Table**: Shows all players' species with body sizes, traits, and food tokens
- **Player Hand**: Displays your available cards for quick reference
- **Messages**: Real-time game events and status messages
- **Food Bank**: Shows current food availability with color-coded indicators
  - 🟢 Green: >10 food (abundant)
  - 🟡 Yellow: 5-10 food (moderate)
  - 🔴 Red: <5 food (scarce)
- **Round Counter**: Track which round you're in
- **Deck Counter**: Visual progress bar showing remaining cards

### 🎴 Card Management
- Dual-sided cards display both options (e.g., "PARASITE / CARNIVORE")
- Easy-to-read card list with numbered selections
- Color-coded player cards (cyan for human player, red for AI)

## How to Run

1. **Start the game**:
   ```bash
   python main.py
   ```

2. **Select number of players** in the startup dialog:
   - 2 Players (You vs AI)
   - 3 Players (You, AI, AI)

3. **The game window opens** and automatically:
   - Initializes your species
   - Deals your starting hand
   - Begins the first round

## Architecture

### New Modules

- **assets/gui_window.py**: Main graphical GUI class using tkinter
- **assets/gui_bridge.py**: Bridge functions to update GUI from game logic
- **assets/game.py**: Updated to work with both terminal and graphical GUIs

### GUI Components

```
┌─────────────────────────────────────────────────────────┐
│  ROUND 1  ⚡                    🌾 Food: 12             │
├──────────────────────┬──────────────────────────────────┤
│                      │                                  │
│  ⚔️ Species Table    │   👤 Your Turn                   │
│                      │                                  │
│  (All Players'       │   🎴 Your Hand                   │
│   Species with       │   1. Card Name                   │
│   Traits, Tokens)    │   2. Card Name / Other Side      │
│                      │   3. Card Name                   │
│                      │                                  │
│                      │   [Play Card] [Skip Turn]        │
│                      │                                  │
│                      │   📢 Messages                    │
│                      │   Game event #1                  │
│                      │   Game event #2                  │
│                      │                                  │
└──────────────────────┴──────────────────────────────────┘
│  Status: Ready                                          │
└─────────────────────────────────────────────────────────┘
```

## Game Flow with GUI

1. **Startup**: Player selection dialog appears
2. **Initialization**: Game window opens, species are created
3. **Main Rounds**:
   - Card play phase (human and AI players take turns)
   - Feeding phase (select species to feed with available food)
   - Carnivore attacks (species attack other players' species)
   - Extinction check (remove unfed species)
4. **Game Over**: Final scores displayed when deck runs out

## Technical Details

### Colors & Styling
- **Background**: #0f1419 (very dark blue)
- **Panel Background**: #1a1a2e (dark blue)
- **Header Background**: #16213e (dark cyan-blue)
- **Player Color**: Cyan (#00d4ff)
- **AI Color**: Red (#ff0000)
- **Success**: Green (#00ff88)
- **Warning**: Gold/Yellow
- **Error**: Red

### Thread Management
- Game runs in a separate daemon thread
- GUI event loop stays responsive
- All updates properly queued to GUI thread

### Unicode Support
- Game names, traits, and icons fully supported
- Proper Windows console encoding handling

## Switching Between Interfaces

The game auto-detects which interface to use:
- **With game_window**: Uses graphical GUI
- **Without game_window**: Falls back to terminal (Rich library)

This allows the same game code to work with both interfaces!

## Future Enhancements

Possible GUI improvements:
- [ ] Drag-and-drop card selection
- [ ] Animated species attacks
- [ ] Game statistics tracker
- [ ] Card analysis/help tooltips
- [ ] Replay and undo functionality
- [ ] Settings panel for game options

## Known Limitations

- Game logic is still primarily AI-controlled; human player interaction is limited to card selection
- Window resizing may require manual layout adjustments
- No save/load game feature yet

## Notes

The graphical GUI is a complete redesign from the text-based interface while maintaining all game logic and mechanics. The underlying Evolution game rules remain unchanged:
- 84-card deck with dual-sided cards
- Species traits and evolution
- Food collection and carnivore attacks
- Extinction mechanics

Enjoy your new graphical Evolution experience!
