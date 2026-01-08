# gui.py - Text-based GUI using Rich library
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.layout import Layout
from rich import box
from rich.style import Style
import os

console = Console()

# Enhanced color scheme
PLAYER_COLOR = "cyan"
AI_COLOR = "red"
ACCENT_COLOR = "magenta"
SUCCESS_COLOR = "green"
WARNING_COLOR = "yellow"
INFO_COLOR = "blue"

# Background colors for better visuals
BG_DARK = "on #1a1a2e"
BG_PANEL = "on #16213e"

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_title(text):
    """Print a centered title with styling."""
    title_text = Text(text, style="bold white on #0f3460")
    console.print(Panel(title_text, style="bold magenta", expand=False, padding=(1, 3)), justify="center")
    console.print()

def print_header(text):
    """Print a section header with better styling."""
    header_panel = Panel(
        Text(text, style="bold white on #16213e"),
        style="bold cyan",
        expand=False,
        padding=(0, 2)
    )
    console.print(header_panel, justify="center")
    console.print()

def print_info(text):
    """Print info message with styling."""
    console.print(f"[cyan]ℹ {text}[/cyan]")

def print_success(text):
    """Print success message with styling."""
    console.print(f"[green]✓ {text}[/green]")

def print_warning(text):
    """Print warning message with styling."""
    console.print(f"[yellow]⚠ {text}[/yellow]")

def print_error(text):
    """Print error message with styling."""
    console.print(f"[red]✗ {text}[/red]")

def show_hand(hand):
    """Display hand as a beautiful formatted table."""
    if not hand:
        print_info("No cards in hand")
        return
    
    table = Table(
        title="🎴 Your Hand",
        box=box.ROUNDED,
        highlight=True,
        title_style="bold cyan on #16213e",
        border_style="bright_cyan",
        header_style="bold white on #0f3460"
    )
    table.add_column("#", style="bold yellow", justify="center")
    table.add_column("Card Name", style="bright_white")
    
    for idx, card in enumerate(hand, 1):
        card_display = str(card)
        table.add_row(str(idx), card_display)
    
    console.print(table)
    console.print()

def show_species_table(players):
    """Display all players' species in a beautiful table."""
    header_panel = Panel(
        Text("⚔️  Current Species", style="bold white on #16213e"),
        style="bold green",
        expand=False,
        padding=(0, 2)
    )
    console.print(header_panel, justify="center")
    console.print()
    
    table = Table(
        box=box.ROUNDED,
        highlight=True,
        border_style="bright_green",
        header_style="bold white on #0f3460"
    )
    table.add_column("Player", style="bold", justify="center")
    table.add_column("Species", style="white")
    
    for player in players:
        player_style = f"bold {PLAYER_COLOR}" if not player.is_ai else f"bold {AI_COLOR}"
        player_name = Text(player.name, style=player_style)
        
        if player.species:
            for idx, species in enumerate(player.species, 1):
                species_text = str(species)
                table.add_row(player_name if idx == 1 else "", species_text)
        else:
            table.add_row(player_name, "[dim](no species)[/dim]")
    
    console.print(table)
    console.print()

def show_player_turn(player):
    """Display player turn header with styling."""
    style = PLAYER_COLOR if not player.is_ai else AI_COLOR
    turn_title = Text(f"→ {player.name}'s Turn ←", style=f"bold {style} on #16213e")
    console.print(Panel(turn_title, style=f"bold {style}", expand=False, padding=(0, 2)), justify="center")
    console.print()

def show_food_bank(food_bank):
    """Display food bank with visual styling."""
    if food_bank > 10:
        food_color = "green"
    elif food_bank > 5:
        food_color = "yellow"
    else:
        food_color = "red"
    
    food_text = Text(f"🌾 Food: {food_bank} chips", style=f"bold {food_color} on #16213e")
    console.print(Panel(food_text, style=food_color, expand=False, padding=(0, 2)), justify="center")
    console.print()

def show_deck_count(remaining, total=84):
    """Display deck information with visual bar."""
    percentage = int((remaining / total) * 100)
    bar_length = 20
    filled = int(bar_length * (remaining / total))
    bar = "█" * filled + "░" * (bar_length - filled)
    deck_text = f"🂠 Deck: {bar} {remaining}/{total}"
    console.print(f"[bright_blue]{deck_text}[/bright_blue]")

def show_round_header(round_number):
    """Display round number with styling."""
    round_text = Text(f"⚡ ROUND {round_number} ⚡", style="bold white on #0f3460")
    console.print(Panel(round_text, style="bold magenta", expand=False, padding=(1, 3)), justify="center")
    console.print()

def show_game_over(winner):
    """Display game over screen with celebration."""
    clear_screen()
    console.print("\n" * 2)
    
    # Victory panel
    victory_text = Text(f"🏆 {winner.name} WINS! 🏆", style="bold gold1 on #0f3460")
    console.print(Panel(
        victory_text,
        style="bold gold1",
        expand=False,
        padding=(2, 20)
    ), justify="center")
    
    console.print("\n" * 2)

def get_yes_no(prompt):
    """Get yes/no input from user with styling."""
    while True:
        console.print(f"\n[bold cyan on #16213e]❓ {prompt} [y/N]: [/bold cyan on #16213e]", end="")
        choice = input().strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no', '']:
            return False
        else:
            print_error("Please enter 'y' or 'n'")

def get_numbered_choice(options, prompt="Choose one", allow_cancel=False):
    """Get numbered choice with beautiful formatting."""
    while True:
        choice_text = Text(prompt, style="bold bright_white on #16213e")
        console.print(Panel(choice_text, style="bright_cyan", expand=False, padding=(0, 2)), justify="center")
        
        # Display options with nice formatting
        for idx, option in enumerate(options, 1):
            display_option = str(option)[:75] + ("..." if len(str(option)) > 75 else "")
            # Alternate colors for better visibility
            color_idx = "bright_cyan" if idx % 2 == 0 else "bright_white"
            console.print(f"  [bold yellow]{idx:2d}[/bold yellow] │ [{color_idx}]{display_option}[/{color_idx}]")
        
        if allow_cancel:
            console.print(f"  [dim]q  │ Cancel[/dim]")
        
        choice = input(f"\n[bold bright_green on #16213e]→ Choose: [/bold bright_green on #16213e]").strip()
        
        if allow_cancel and choice.lower() == 'q':
            return None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
        
        print_error("Invalid choice, please try again")

def get_card_choice(hand, prompt="Play card"):
    """Get card choice from player's hand (assumes hand is already displayed)."""
    while True:
        choice = input(f"[bold bright_green on #16213e]{prompt} (1-{len(hand)} or 'q' to skip): [/bold bright_green on #16213e]").strip()
        
        if choice.lower() == 'q':
            return None
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(hand):
                return idx
        
        print_error("Invalid choice, please try again")

def show_options(options, prompt="Choose action"):
    """Display multiple options and get selection with styling."""
    return get_numbered_choice(options, prompt)

def show_species_options(player, prompt="Choose target species"):
    """Let player choose one of their species with styling."""
    if not player.species:
        print_warning("You have no species!")
        return None
    
    while True:
        choice_text = Text(prompt, style="bold bright_white on #16213e")
        console.print(Panel(choice_text, style="bright_magenta", expand=False, padding=(0, 2)), justify="center")
        
        for idx, species in enumerate(player.species, 1):
            console.print(f"  [bold yellow]{idx:2d}[/bold yellow] │ {species}")
        console.print(f"  [bold yellow]0 [/bold yellow] │ [dim]Create new species[/dim]")
        
        choice = input(f"\n[bold bright_green on #16213e]→ Choose: [/bold bright_green on #16213e]").strip()
        
        if choice == '0':
            return 0
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(player.species):
                return idx + 1
        
        print_error("Invalid choice, please try again")

def show_opponent_selection(current_player, players):
    """Let player choose an opponent with styling."""
    opponents = [p for p in players if p != current_player and p.species]
    
    if not opponents:
        print_warning("No opponents with species to target!")
        return None
    
    while True:
        choice_text = Text("Choose opponent", style="bold bright_white on #16213e")
        console.print(Panel(choice_text, style="bright_red", expand=False, padding=(0, 2)), justify="center")
        
        for idx, opponent in enumerate(opponents, 1):
            style = "bright_cyan" if not opponent.is_ai else "bright_red"
            console.print(f"  [bold yellow]{idx:2d}[/bold yellow] │ [{style}]{opponent.name}[/{style}]")
        
        choice = input(f"\n[bold bright_green on #16213e]→ Choose: [/bold bright_green on #16213e]").strip()
        
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(opponents):
                return opponents[idx]
        
        print_error("Invalid choice, please try again")

def pause_for_input(message="Press Enter to continue..."):
    """Pause and wait for user input with styling."""
    input(f"\n[dim bold bright_cyan]{message}[/dim bold bright_cyan]")
