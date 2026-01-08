# gui_window.py - Completely redesigned single-window GUI
import tkinter as tk
from tkinter import ttk
import threading

class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Russian Evolution - Card Game")
        self.root.geometry("1600x950")
        self.root.configure(bg="#0f1419")
        
        # Protocol handling
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._running = True
        
        # Input handling - using threading Event for proper blocking
        self._choice_result = None
        self._choice_event = threading.Event()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0f1419')
        style.configure('TLabel', background='#0f1419', foreground='#ffffff')
        style.configure('Header.TLabel', background='#0f1419', foreground='#00d4ff', font=('Arial', 13, 'bold'))
        style.configure('Title.TLabel', background='#0f1419', foreground='#ff00ff', font=('Arial', 16, 'bold'))
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI layout."""
        # === TOP BAR ===
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=15, pady=12)
        
        self.round_label = ttk.Label(top_frame, text="ROUND 1", style='Title.TLabel')
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.food_label = ttk.Label(top_frame, text="Food: 0", style='Header.TLabel', font=('Arial', 13))
        self.food_label.pack(side=tk.RIGHT, padx=20)
        
        # === MAIN CONTENT AREA ===
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # LEFT: Species Table (larger)
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))
        
        species_label = ttk.Label(left_frame, text="Species Table", style='Header.TLabel')
        species_label.pack(anchor=tk.W, pady=(0, 8))
        
        species_scroll = ttk.Scrollbar(left_frame)
        species_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.species_text = tk.Text(
            left_frame,
            bg='#1a1a2e',
            fg='#00d4ff',
            font=('Courier', 9),
            yscrollcommand=species_scroll.set,
            wrap=tk.WORD
        )
        self.species_text.pack(fill=tk.BOTH, expand=True)
        species_scroll.config(command=self.species_text.yview)
        
        # RIGHT: Hand, Actions, Messages
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(12, 0))
        
        # Hand display
        hand_label = ttk.Label(right_frame, text="Your Hand", style='Header.TLabel')
        hand_label.pack(anchor=tk.W, pady=(0, 6))
        
        hand_frame = ttk.Frame(right_frame)
        hand_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        hand_scroll = ttk.Scrollbar(hand_frame)
        hand_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hand_listbox = tk.Listbox(
            hand_frame,
            bg='#16213e',
            fg='#00ff88',
            font=('Arial', 9),
            yscrollcommand=hand_scroll.set,
            height=6
        )
        self.hand_listbox.pack(fill=tk.BOTH, expand=True)
        hand_scroll.config(command=self.hand_listbox.yview)
        
        # ACTION PANEL (Dynamic)
        action_label = ttk.Label(right_frame, text="Actions", style='Header.TLabel')
        action_label.pack(anchor=tk.W, pady=(10, 6))
        
        action_frame = ttk.Frame(right_frame)
        action_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 10))
        
        action_scroll = ttk.Scrollbar(action_frame)
        action_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.action_canvas = tk.Canvas(
            action_frame,
            bg='#16213e',
            highlightthickness=0,
            yscrollcommand=action_scroll.set
        )
        self.action_canvas.pack(fill=tk.BOTH, expand=True)
        action_scroll.config(command=self.action_canvas.yview)
        
        self.action_frame_inner = ttk.Frame(self.action_canvas)
        self.action_canvas.create_window((0, 0), window=self.action_frame_inner, anchor='nw')
        self.action_frame_inner.bind(
            "<Configure>",
            lambda e: self.action_canvas.configure(scrollregion=self.action_canvas.bbox("all"))
        )
        
        # MESSAGE LOG
        msg_label = ttk.Label(right_frame, text="Messages", style='Header.TLabel')
        msg_label.pack(anchor=tk.W, pady=(0, 6))
        
        msg_frame = ttk.Frame(right_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        
        msg_scroll = ttk.Scrollbar(msg_frame)
        msg_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_text = tk.Text(
            msg_frame,
            height=8,
            bg='#16213e',
            fg='#ffff00',
            font=('Courier', 8),
            yscrollcommand=msg_scroll.set,
            wrap=tk.WORD
        )
        self.message_text.pack(fill=tk.BOTH, expand=True)
        msg_scroll.config(command=self.message_text.yview)
        
        # STATUS BAR
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=15, pady=8)
        
        self.status_label = ttk.Label(status_frame, text="Ready", style='Header.TLabel')
        self.status_label.pack(side=tk.LEFT)
    
    def show_choices(self, prompt, options):
        """Show numbered action buttons instead of popup dialog."""
        # Clear previous actions
        for widget in self.action_frame_inner.winfo_children():
            widget.destroy()
        
        # Show prompt
        prompt_label = tk.Label(
            self.action_frame_inner,
            text=prompt,
            bg='#16213e',
            fg='#00d4ff',
            font=('Arial', 10, 'bold'),
            wraplength=350,
            justify=tk.LEFT
        )
        prompt_label.pack(fill=tk.X, padx=5, pady=(5, 10))
        
        # Create buttons for each option
        self._choice_result = None
        self._choice_event.clear()  # Reset event
        
        def select_option(idx):
            self._choice_result = idx
            self._choice_event.set()  # Signal that choice is made
            # Disable all buttons
            for btn in option_buttons:
                btn.config(state=tk.DISABLED)
        
        option_buttons = []
        for idx, option in enumerate(options):
            btn = tk.Button(
                self.action_frame_inner,
                text=f"{idx+1}. {str(option)[:50]}",
                bg="#005577" if idx % 2 == 0 else "#003d54",
                fg="#00d4ff",
                activebackground="#00d4ff",
                activeforeground="#000000",
                font=('Arial', 9),
                command=lambda i=idx: select_option(i),
                wraplength=330,
                justify=tk.LEFT,
                padx=8,
                pady=6,
                anchor=tk.W
            )
            btn.pack(fill=tk.X, padx=5, pady=3)
            option_buttons.append(btn)
        
        # Scroll to top
        self.action_canvas.yview_moveto(0)
        
        # Wait for selection (BLOCKING - proper synchronization)
        self._wait_for_choice()
        return self._choice_result
    
    def _wait_for_choice(self):
        """BLOCKING wait for user to make a choice."""
        # This waits for the choice event to be set by button click
        # while keeping the GUI responsive
        while not self._choice_event.is_set():
            self.root.update()  # Process GUI events
            if not self._running:  # Exit if window closed
                break
    
    def get_input_sync(self, prompt, options):
        """Synchronous input from GUI action panel."""
        return self.show_choices(prompt, options)
    
    def update_round(self, round_num):
        """Update round display."""
        self.round_label.config(text=f"ROUND {round_num}")
    
    def update_food(self, amount):
        """Update food display."""
        color = "green" if amount > 10 else "gold" if amount > 5 else "red"
        self.food_label.config(text=f"Food: {amount}", foreground=color)
    
    def update_species(self, species_text):
        """Update species table."""
        self.species_text.config(state=tk.NORMAL)
        self.species_text.delete(1.0, tk.END)
        self.species_text.insert(tk.END, species_text)
        self.species_text.config(state=tk.DISABLED)
    
    def update_hand(self, hand_cards):
        """Update player hand display."""
        self.hand_listbox.delete(0, tk.END)
        for idx, card in enumerate(hand_cards, 1):
            self.hand_listbox.insert(tk.END, f"{idx}. {card}")
    
    def add_message(self, message, color="yellow"):
        """Add message to message log."""
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"{message}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.NORMAL)
    
    def on_closing(self):
        """Handle window closing."""
        self._running = False
        self.root.destroy()

def create_game_window():
    """Create and return the game window."""
    root = tk.Tk()
    window = GameWindow(root)
    root.update()
    return root, window
