# gui_window.py - Graphical GUI using tkinter
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import font as tkFont
import threading

class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Russian Evolution - Card Game")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f1419")
        
        # Make tkinter event loop responsive
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._running = True
        
        # Input handling
        self._input_result = None
        self._waiting_for_input = False
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#0f1419')
        style.configure('TLabel', background='#0f1419', foreground='#ffffff')
        style.configure('Header.TLabel', background='#0f1419', foreground='#00d4ff', font=('Arial', 14, 'bold'))
        style.configure('Title.TLabel', background='#0f1419', foreground='#ff00ff', font=('Arial', 16, 'bold'))
        style.configure('TButton', font=('Arial', 10))
        style.map('TButton',
                  foreground=[('pressed', '#000000'), ('active', '#ffffff')],
                  background=[('pressed', '#00d4ff'), ('active', '#005577')])
        
        # Main layout
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI layout."""
        # Top bar - Round and Food Bank
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.round_label = ttk.Label(top_frame, text="ROUND 1", style='Title.TLabel')
        self.round_label.pack(side=tk.LEFT, padx=20)
        
        self.food_label = ttk.Label(top_frame, text="🌾 Food: 0", style='Header.TLabel', font=('Arial', 12))
        self.food_label.pack(side=tk.RIGHT, padx=20)
        
        # Main content - Split into left (table) and right (hand + actions)
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT SIDE - Species Table
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        species_label = ttk.Label(left_frame, text="⚔️ Species Table", style='Header.TLabel')
        species_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Species display with scrollbar
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.species_text = tk.Text(
            tree_frame,
            height=20,
            width=50,
            bg='#1a1a2e',
            fg='#00d4ff',
            font=('Courier', 9),
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        self.species_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.species_text.yview)
        
        # RIGHT SIDE - Player Hand and Actions
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
        
        # Player info
        player_label = ttk.Label(right_frame, text="👤 Your Turn", style='Header.TLabel')
        player_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Hand display
        hand_label = ttk.Label(right_frame, text="🎴 Your Hand", style='Header.TLabel', font=('Arial', 11, 'bold'))
        hand_label.pack(anchor=tk.W, pady=(10, 5))
        
        hand_frame = ttk.Frame(right_frame)
        hand_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        hand_scrollbar = ttk.Scrollbar(hand_frame)
        hand_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.hand_listbox = tk.Listbox(
            hand_frame,
            bg='#16213e',
            fg='#00ff88',
            font=('Arial', 10),
            yscrollcommand=hand_scrollbar.set,
            selectmode=tk.SINGLE,
            activestyle='none'
        )
        self.hand_listbox.pack(fill=tk.BOTH, expand=True)
        hand_scrollbar.config(command=self.hand_listbox.yview)
        self.hand_listbox.bind('<<ListboxSelect>>', self.on_card_selected)
        
        # Action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.play_btn = ttk.Button(button_frame, text="Play Card")
        self.play_btn.pack(fill=tk.X, pady=5)
        
        self.skip_btn = ttk.Button(button_frame, text="Skip Turn")
        self.skip_btn.pack(fill=tk.X, pady=5)
        
        # Message area
        msg_label = ttk.Label(right_frame, text="📢 Messages", style='Header.TLabel', font=('Arial', 11, 'bold'))
        msg_label.pack(anchor=tk.W, pady=(10, 5))
        
        msg_frame = ttk.Frame(right_frame)
        msg_frame.pack(fill=tk.BOTH, expand=True)
        
        msg_scrollbar = ttk.Scrollbar(msg_frame)
        msg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.message_text = tk.Text(
            msg_frame,
            height=8,
            bg='#16213e',
            fg='#ffff00',
            font=('Courier', 8),
            yscrollcommand=msg_scrollbar.set,
            wrap=tk.WORD
        )
        self.message_text.pack(fill=tk.BOTH, expand=True)
        msg_scrollbar.config(command=self.message_text.yview)
        
        # Status bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready", style='Header.TLabel')
        self.status_label.pack(side=tk.LEFT)
        
    def update_round(self, round_num):
        """Update round display."""
        self.round_label.config(text=f"⚡ ROUND {round_num} ⚡")
    
    def update_food(self, amount):
        """Update food bank display."""
        color = "green" if amount > 10 else "gold" if amount > 5 else "red"
        self.food_label.config(text=f"🌾 Food: {amount}", foreground=color)
    
    def update_species(self, species_text):
        """Update species table display."""
        self.species_text.config(state=tk.NORMAL)
        self.species_text.delete(1.0, tk.END)
        self.species_text.insert(tk.END, species_text)
        self.species_text.config(state=tk.DISABLED)
    
    def update_hand(self, hand_cards):
        """Update hand display."""
        self.hand_listbox.delete(0, tk.END)
        for idx, card in enumerate(hand_cards, 1):
            self.hand_listbox.insert(tk.END, f"{idx}. {card}")
    
    def add_message(self, message, color="yellow"):
        """Add a message to the message area."""
        self.message_text.config(state=tk.NORMAL)
        self.message_text.insert(tk.END, f"{message}\n")
        self.message_text.see(tk.END)
        self.message_text.config(state=tk.NORMAL)
    
    def on_card_selected(self, event):
        """Handle card selection."""
        if self.hand_listbox.curselection():
            idx = self.hand_listbox.curselection()[0]
            self.add_message(f"Selected card {idx + 1}", "cyan")
    
    def show_choice_dialog(self, title, options):
        """Show a dialog for choosing from options."""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("450x500")
        dialog.configure(bg="#0f1419")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=title, style='Header.TLabel').pack(pady=10)
        
        result = [None]
        
        def select_option(idx):
            result[0] = idx
            dialog.destroy()
        
        # Create scrollable frame
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(btn_frame, bg="#1a1a2e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(btn_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for idx, option in enumerate(options):
            btn = tk.Button(
                scrollable_frame,
                text=f"{idx+1}. {str(option)[:60]}",
                bg="#005577" if idx % 2 == 0 else "#003d54",
                fg="#00d4ff",
                activebackground="#00d4ff",
                activeforeground="#000000",
                font=('Arial', 9),
                command=lambda i=idx: select_option(i),
                wraplength=380,
                justify=tk.LEFT,
                padx=10,
                pady=8,
                anchor=tk.W
            )
            btn.pack(fill=tk.X, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        dialog.wait_window()
        return result[0]
    
    def get_input_sync(self, prompt, options):
        """Synchronously get user input from GUI."""
        return self.show_choice_dialog(prompt, options)
        
        dialog.wait_window()
        return result[0]
    
    def show_message(self, title, message):
        """Show a message dialog."""
        messagebox.showinfo(title, message)
    
    def show_error(self, title, message):
        """Show an error dialog."""
        messagebox.showerror(title, message)
    
    def on_closing(self):
        """Handle window closing."""
        self._running = False
        self.root.destroy()

def create_game_window():
    """Create and return the game window."""
    root = tk.Tk()
    window = GameWindow(root)
    
    # Make sure the window stays responsive during game loop
    root.update()
    
    return root, window
