import argparse
import customtkinter as ctk
from .gui import MineGameUI

def main():
    parser = argparse.ArgumentParser(description="Modern Minesweeper with Solver")
    parser.add_argument('--size', type=int, default=16, help="Grid size (default: 16)")
    parser.add_argument('--mines', type=int, default=40, help="Number of mines (default: 40)")
    args = parser.parse_args()

    ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    root = ctk.CTk()
    app = MineGameUI(root, n=args.size, k=args.mines)
    root.mainloop()

if __name__ == "__main__":
    main()
