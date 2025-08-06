import tkinter as tk
from tkinter import messagebox
import random
from queue import Queue

class MineGameUI:
    def __init__(self, root, n, k, matrix, mask_mat):
        self.root = root
        self.n = n
        self.k = k
        self.matrix = matrix
        self.mask_mat = mask_mat
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        self.score = 0
        self.flags_left = k
        self.last_clicked = None
        self.cell_q = Queue()

        self.root.title("Minesweeper Test UI")

        self.status = tk.Label(root, text=f"Score: {self.score} | Flags left: {self.flags_left}")
        self.status.pack()

        self.board = tk.Frame(root)
        self.board.pack()

        for r in range(n):
            for c in range(n):
                btn = tk.Button(self.board, width=3, height=1, command=lambda r=r, c=c: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.right_click(r, c))  # Right click
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn


    def colored_button(self, r, c):
        if self.matrix[r][c] == 0:
            self.buttons[r][c]['bg'] = 'gray'        
        elif self.matrix[r][c] == 1:
            self.buttons[r][c]['bg'] = 'green'        
        elif self.matrix[r][c] == 2:
            self.buttons[r][c]['bg'] = 'yellowgreen'        
        elif self.matrix[r][c] == 3:
            self.buttons[r][c]['bg'] = 'gold'
        elif self.matrix[r][c] == 4:
            self.buttons[r][c]['bg'] = 'orange'
        elif self.matrix[r][c] == 5:
            self.buttons[r][c]['bg'] = 'red'

    def reset(self):
        pass

    def bfs(self, r, c):
        if self.mask_mat[r][c] == 1 or self.matrix[r][c] == -1:
            return
        self.mask_mat[r][c] = 1
        self.colored_button(r, c)
        self.buttons[r][c]['text'] = str(self.matrix[r][c]) if self.matrix[r][c] > 0 else ''
        self.buttons[r][c]['relief'] = tk.SUNKEN
        self.score += 1
        self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"
        # item = self.cell_q.get()
        moves = {(0, -1), (-1, 0), (1, 0), (0, 1)}
        for x, y in moves:
                i = r + x
                j = c + y
                if i < 0 or j < 0 or i == self.n or j == self.n:
                    continue

                if self.matrix[i][j] == 0:
                    self.bfs(i,j)
                else:
                    self.mask_mat[i][j] = 1
                    self.colored_button(i, j)
                    self.buttons[i][j]['text'] = str(self.matrix[i][j]) if self.matrix[i][j] > 0 else ''
                    self.buttons[i][j]['relief'] = tk.SUNKEN
                    self.score += 1
                    self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"

    def left_click(self, r, c):
        if self.mask_mat[r][c] != 0: return  # Already revealed or flagged

        if self.matrix[r][c] == -1:
            self.buttons[r][c]['text'] = 'B'
            self.buttons[r][c]['bg'] = 'red'
            self.reveal_all()
            messagebox.showinfo("Game Over", "You clicked a bomb!")
            self.reset()
        elif self.matrix[r][c] == 0:
            self.bfs(r, c)
        else:
            self.colored_button(r, c)
            self.buttons[r][c]['text'] = str(self.matrix[r][c]) if self.matrix[r][c] > 0 else ''
            self.buttons[r][c]['relief'] = tk.SUNKEN
            self.score += 1
            self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"

        self.last_clicked = (r, c)
        self.mask_mat[r][c] = 1
        print(f"Clicked: {r}, {c}")

    def right_click(self, r, c):
        if self.mask_mat[r][c] == 0 and self.flags_left > 0:
            self.mask_mat[r][c] = 2
            self.matrix[r][c] = 2
            self.buttons[r][c]['text'] = 'F'
            self.flags_left -= 1
        elif self.mask_mat[r][c] == 2:
            self.mask_mat[r][c] = 0
            self.matrix[r][c] = 0
            self.buttons[r][c]['text'] = ''
            self.flags_left += 1

        self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"

    def reveal_all(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.matrix[r][c] == -1:
                    self.buttons[r][c]['text'] = 'B'
                    self.buttons[r][c]['bg'] = 'red'

# Helper to create a sample board
class mine:
    def __init__(self, n, k):
        self.k = k
        self.n = n
        self.mask_mat =  [[0 for _ in range(n)] for _ in range(n)]
        self.matrix =  [[0 for _ in range(n)] for _ in range(n)]

    def generate_sample_game(self):
        bombs = random.sample(range(self.n * self.n), self.k)
        for idx in bombs:
            r, c = divmod(idx, n)
            self.matrix[r][c] = -1

            # Update adjacent tiles
            for i in range(max(0, r-1), min(n, r+2)):
                for j in range(max(0, c-1), min(n, c+2)):
                    if self.matrix[i][j] != -1:
                        self.matrix[i][j] += 1
        return self.matrix, self.mask_mat

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    n = 16  # grid size
    k = 40  # bombs
    game = mine(n , k)
    matrix, mask_mat = game.generate_sample_game()
    game = MineGameUI(root, n, k, matrix, mask_mat)
    root.mainloop()
