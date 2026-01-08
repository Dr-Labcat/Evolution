# GUI Improvements - Text-Based Terminal UI

## Overview
The game now features a modern, presentable text-based GUI using the **Rich** library, providing:

- **Formatted tables** for displaying species and cards
- **Color-coded messages** for different event types (success, warning, error, info)
- **Clear visual hierarchy** with panels and headers
- **Responsive layout** that adapts to terminal size
- **Better readability** with organized information display

## Key Features

### 1. **Game Setup**
- Interactive selection menu for number of players (2 or 3)
- Clear welcome screen with game title

### 2. **Card Play Phase**
- **Hand Display**: Your cards shown in a formatted table with indices
- **Species Overview**: All players' current species displayed in organized table
- **Turn Indicator**: Clear visual separation of whose turn it is
- **Input Validation**: Guided choice selection with error messages

### 3. **Feeding Phase**
- **Food Bank Display**: Shows available food tokens
- **Species List**: Formatted table of available species to feed
- **Deck Tracking**: Card count shown for remaining cards in deck

### 4. **Round Management**
- **Round Header**: Clearly shows which round is being played
- **Phase Headers**: Distinct sections for Card Play, Feeding, and Carnivore Attacks
- **Status Messages**: Color-coded feedback for all actions

### 5. **Game End**
- **Winner Display**: Prominent announcement with trophy symbol
- **Final Scores**: Organized display of all players' final points

## Color Scheme

- **Cyan**: Player information and selections
- **Red**: AI player information  
- **Blue**: Informational headers and section dividers
- **Green**: Success messages and confirmations
- **Yellow**: Warnings and food bank information
- **Magenta**: Important trait-related messages

## New Functions in `assets/gui.py`

### Display Functions
- `print_title(text)` - Display centered title
- `print_header(text)` - Display section header
- `print_info(text)` - Blue informational message
- `print_success(text)` - Green success message with checkmark
- `print_warning(text)` - Yellow warning message
- `print_error(text)` - Red error message with X mark
- `show_hand(hand)` - Display player's hand in formatted table
- `show_species_table(players)` - Display all players' species
- `show_player_turn(player)` - Highlight whose turn it is
- `show_food_bank(amount)` - Display food bank status
- `show_round_header(round_number)` - Display current round
- `show_game_over(winner)` - Display game over screen

### Input Functions
- `get_numbered_choice(options, prompt, allow_cancel)` - Get selection from numbered list
- `get_card_choice(hand, prompt)` - Get card selection from hand
- `show_opponent_selection(player, players)` - Select an opponent
- `show_options(options, prompt)` - Display and get selection from options
- `pause_for_input(message)` - Wait for user to press Enter

## Integration with Game Logic

The GUI module is integrated into:
- `main.py` - Game initialization and menu
- `assets/game.py` - All game phases and player interactions

All print statements and basic input() calls have been replaced with Rich-based GUI functions for consistent, professional appearance.

## Installation

The Rich library is already installed. To install in a fresh environment:
```bash
pip install rich
```

## Usage

Run the game as normal:
```bash
python main.py
```

The game will now display with the improved terminal UI!
