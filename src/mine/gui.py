import customtkinter as ctk
from PIL import Image
import os
import threading
import time
from .game import MinesweeperGame
from .solver import MinesweeperSolver

class MineGameUI:
    def __init__(self, root, n=16, k=40):
        self.root = root
        self.default_n = n
        self.default_k = k
        self.n = n
        self.k = k
        
        self.game = None
        self.solver = MinesweeperSolver()
        self.buttons = []
        self.is_solving = False
        self.stop_solving = False
        
        self.root.title("Modern Minesweeper")
        
        # Load Assets
        asset_path = os.path.join(os.path.dirname(__file__), 'assets')
        self.bomb_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'bomb.png')), size=(20, 20))
        self.flag_icon = ctk.CTkImage(Image.open(os.path.join(asset_path, 'flag.png')), size=(20, 20))

        self._setup_ui()
        self.start_game(n, k)

    def _setup_ui(self):
        # Top Bar
        self.top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Left side: Difficulty
        self.diff_var = ctk.StringVar(value="Medium")
        self.diff_menu = ctk.CTkOptionMenu(
            self.top_frame, 
            values=["Easy", "Medium", "Hard"],
            command=self.change_difficulty,
            variable=self.diff_var,
            width=100
        )
        self.diff_menu.pack(side="left", padx=(0, 20))

        # Score / Status
        self.score_label = ctk.CTkLabel(
            self.top_frame, 
            text=f"Flags: 0", 
            font=("Roboto", 20, "bold"),
            text_color="#E0E0E0"
        )
        self.score_label.pack(side="left")

        # Right side: Controls
        self.restart_btn = ctk.CTkButton(self.top_frame, text="New Game", command=self.reset_game, width=100, fg_color="#3B8ED0", hover_color="#36719F")
        self.restart_btn.pack(side="right", padx=(10, 0))

        self.solve_btn = ctk.CTkButton(self.top_frame, text="Auto Solve", command=self.toggle_solve, width=100, fg_color="#2CC985", hover_color="#25A970")
        self.solve_btn.pack(side="right", padx=(10, 0))

        self.hint_btn = ctk.CTkButton(self.top_frame, text="Hint", command=self.show_hint, width=80, fg_color="#E2B340", hover_color="#C49B36")
        self.hint_btn.pack(side="right", padx=(0, 0))

        # Game Grid Container
        self.grid_container = ctk.CTkFrame(self.root, fg_color="#2B2B2B", corner_radius=10)
        self.grid_container.pack(expand=True, fill="both", padx=20, pady=(0, 20))

    def start_game(self, n, k):
        self.n = n
        self.k = k
        self.game = MinesweeperGame(n, k)
        self.is_solving = False
        self.stop_solving = False
        self.solve_btn.configure(text="Auto Solve", fg_color="#2CC985")
        
        # Resize window based on grid size
        # Base size + grid size * cell size
        width = max(600, n * 35 + 60)
        height = n * 35 + 120
        self.root.geometry(f"{width}x{height}")

        # Clear existing grid
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        
        # Configure grid weights
        for i in range(n):
            self.grid_container.grid_rowconfigure(i, weight=1)
            self.grid_container.grid_columnconfigure(i, weight=1)

        # Create buttons
        for r in range(n):
            for c in range(n):
                btn = ctk.CTkButton(
                    self.grid_container, 
                    text="", 
                    width=30, 
                    height=30, 
                    corner_radius=4,
                    fg_color="#4A4A4A",
                    hover_color="#5A5A5A",
                    command=lambda r=r, c=c: self.on_left_click(r, c)
                )
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                self.buttons[r][c] = btn
        
        self._update_status()

    def change_difficulty(self, choice):
        if choice == "Easy":
            self.start_game(9, 10)
        elif choice == "Medium":
            self.start_game(16, 40)
        elif choice == "Hard":
            self.start_game(30, 99) # Standard Hard is often 30x16, but let's do square 20x20 or keep it square for simplicity? 
            # Standard Minesweeper Hard is 30x16. My logic supports rectangular, but let's stick to square for now to keep UI simple or adapt.
            # Let's do 24x24 for Hard to fit nicely on screen.
            self.start_game(24, 99)

    def reset_game(self):
        # Restart with current settings
        self.start_game(self.n, self.k)

    def on_left_click(self, r, c):
        if self.game.game_over:
            return
        
        safe = self.game.reveal(r, c)
        self._refresh_grid_optimized()
        self._update_status()
        
        if not safe:
            self._show_game_over(won=False)
        elif self.game.won:
            self._show_game_over(won=True)

    def on_right_click(self, r, c):
        if self.game.game_over:
            return
            
        self.game.toggle_flag(r, c)
        self._refresh_grid_optimized()
        self._update_status()

    def _refresh_grid_optimized(self):
        # Only update cells that have changed state visually
        state = self.game.get_state()
        for r in range(self.n):
            for c in range(self.n):
                val = state[r][c]
                btn = self.buttons[r][c]
                
                # Check current visual state to avoid unnecessary configures (flickering)
                current_text = btn.cget("text")
                current_image = btn.cget("image")
                current_fg = btn.cget("fg_color")
                
                target_text = ""
                target_image = None
                target_fg = "#4A4A4A"
                target_state = "normal"
                target_text_color = "white"

                if val == -2: # Hidden
                    target_fg = "#4A4A4A"
                elif val == -1: # Flagged or Mine
                    if self.game.game_over and (r, c) in self.game.mines_loc:
                         target_image = self.bomb_icon
                         target_fg = "#D32F2F" # Red
                         target_state = "disabled"
                    else:
                        target_image = self.flag_icon
                        target_fg = "#4A4A4A"
                else: # Revealed
                    target_fg = "#2B2B2B" # Darker background for revealed
                    target_state = "disabled"
                    if val > 0:
                        target_text = str(val)
                        # Modern Colors
                        if val == 1: target_text_color = "#4285F4" # Blue
                        elif val == 2: target_text_color = "#34A853" # Green
                        elif val == 3: target_text_color = "#EA4335" # Red
                        elif val == 4: target_text_color = "#A142F4" # Purple
                        elif val == 5: target_text_color = "#FA7B17" # Orange
                        elif val == 6: target_text_color = "#00ACC1" # Cyan
                        elif val == 7: target_text_color = "#333333" # Black/Dark
                        elif val == 8: target_text_color = "#9E9E9E" # Gray

                # Apply changes only if needed
                if current_text != target_text or str(current_image) != str(target_image) or current_fg != target_fg:
                     btn.configure(
                         text=target_text, 
                         image=target_image, 
                         fg_color=target_fg, 
                         state=target_state,
                         text_color=target_text_color
                     )

    def _update_status(self):
        self.score_label.configure(text=f"Flags: {self.game.flags_left}")

    def _show_game_over(self, won):
        title = "Victory!" if won else "Game Over"
        color = "#2CC985" if won else "#D32F2F"
        self.score_label.configure(text=f"{title}", text_color=color)
        self.is_solving = False
        self.stop_solving = True
        self.solve_btn.configure(text="Auto Solve", fg_color="#2CC985")

    def show_hint(self):
        if self.game.game_over: return
        action, r, c = self.solver.get_next_move(self.game.get_state(), self.game.flags_left)
        if action:
            self.buttons[r][c].configure(fg_color="#E2B340") # Highlight
            self.root.after(500, lambda: self._refresh_grid_optimized())
        else:
            # self.score_label.configure(text="No obvious moves.")
            pass

    def toggle_solve(self):
        if self.is_solving:
            self.stop_solving = True
            self.is_solving = False
            self.solve_btn.configure(text="Auto Solve", fg_color="#2CC985")
        else:
            self.is_solving = True
            self.stop_solving = False
            self.solve_btn.configure(text="Stop", fg_color="#D32F2F")
            self._solve_step()

    def _solve_step(self):
        if self.stop_solving or self.game.game_over:
            self.is_solving = False
            self.solve_btn.configure(text="Auto Solve", fg_color="#2CC985")
            return

        action, r, c = self.solver.get_next_move(self.game.get_state(), self.game.flags_left)
        
        if action == 'REVEAL':
            self.on_left_click(r, c)
        elif action == 'FLAG':
            self.on_right_click(r, c)
        else:
            # No move found
            self.is_solving = False
            self.solve_btn.configure(text="Auto Solve", fg_color="#2CC985")
            return

        # Faster speed: 50ms
        self.root.after(50, self._solve_step)

