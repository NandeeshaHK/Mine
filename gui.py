import tkinter as tk
from tkinter import messagebox
import random
from collections import deque

class MineGameUI:
    def __init__(self, root, n, k):
        self.root = root
        self.n = n
        self.k = k
        self.matrix = [[0 for _ in range(n)] for _ in range(n)]
        self.mask_mat = [[0 for _ in range(n)] for _ in range(n)]
        self.buttons = [[None for _ in range(n)] for _ in range(n)]
        self.score = 0
        self.flags_left = k
        self.last_clicked = None
        self.first_click  = True
        self.moves = {(0, -1), (-1, 0), (1, 0), (0, 1)}

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
        if   self.matrix[r][c] == 0:
            self.buttons[r][c]['bg'] = 'gray'        
        elif self.matrix[r][c] == 1:
            self.buttons[r][c]['bg'] = 'green'        
        elif self.matrix[r][c] == 2:
            self.buttons[r][c]['bg'] = 'yellowgreen'        
        elif self.matrix[r][c] == 3:
            self.buttons[r][c]['bg'] = 'gold'
        elif self.matrix[r][c] == 4:
            self.buttons[r][c]['bg'] = 'orange'
        elif self.matrix[r][c] >= 5:
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
        for x, y in self.moves:
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
    
    def check(self):
        # print()
        # for i in range(self.n):
        #     for j in range(self.n):
        #         print(f"{self.mask_mat[i][j]}  ", end='')
        #     print()
        # print()
        # for i in range(self.n):
        #     for j in range(self.n):
        #         print(f"{self.matrix[i][j]}  ", end='')
        #     print()
        # print(self.bombs)
        for i in range(self.n):
            for j in range(self.n):
                if self.mask_mat[i][j] == -1:
                    if self.mask_mat[i][j] != self.matrix[i][j]:
                        messagebox.showinfo("Game Over", "You have Low IQ. You should be flagged!")
                        return
                    
        # self.reveal_all()
        messagebox.showinfo("Game Finished", "You are BOMB!")
        self.reset()
        return True
    
    def is_cell_true(self, r, c):
        '''
        This function returns true, if the cell number is equal to the number of flags around it        
        '''

        count = 0
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.mask_mat[i][j] == -1:
                    count += 1
        # print(count)
        return count == self.matrix[r][c]
    
    def left_click(self, r, c):
        if self.flags_left == 0:
            self.check()

        self.start_friendly_generate_bombs(r, c)

        if self.mask_mat[r][c] == 0: # Already revealed or flagged
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
        elif self.mask_mat[r][c] == -1:
            return
        elif self.mask_mat[r][c] == 1:
            print(self.is_cell_true(r, c))
            if self.is_cell_true(r, c):
                for i in range(max(0, r-1), min(self.n, r+2)):
                    for j in range(max(0, c-1), min(self.n, c+2)):
                        if self.mask_mat[i][j] == -1:
                            if self.mask_mat[i][j] != self.matrix[i][j]:
                                self.buttons[i][i]['text'] = 'B'
                                self.buttons[j][j]['bg'] = 'red'
                                self.reveal_all()
                                messagebox.showinfo("Game Over", "You have Low IQ. You should be flagged!")
                                self.reset()
                                return
                        else:
                            self.colored_button(i, j)
                            self.buttons[i][j]['text'] = str(self.matrix[i][j]) if self.matrix[i][j] > 0 else ''
                            self.buttons[i][j]['relief'] = tk.SUNKEN
                            self.score += 1
                            self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"

        self.last_clicked = (r, c)
        self.mask_mat[r][c] = 1
        print(f"Clicked: {r}, {c}")

    def right_click(self, r, c):
        if self.mask_mat[r][c] == 0 and self.flags_left > 0:
            self.mask_mat[r][c] = -1
            self.buttons[r][c]['text'] = 'F'
            self.buttons[r][c]['bg'] = 'black'
            self.flags_left -= 1
        elif self.mask_mat[r][c] == -1:
            self.mask_mat[r][c] = 0
            self.buttons[r][c]['text'] = ''
            self.buttons[r][c]['bg'] = 'white'
            self.flags_left += 1

        self.status['text'] = f"Score: {self.score} | Flags left: {self.flags_left}"

    def reveal_all(self):
        for r in range(self.n):
            for c in range(self.n):
                if self.matrix[r][c] == -1:
                    self.buttons[r][c]['text'] = 'B'
                    self.buttons[r][c]['bg'] = 'red'
    
    def start_friendly_generate_bombs(self, r, c):
        if self.n < 5:
            messagebox.showinfo("Box count should be greater or equal to 5")
            exit(0)
            return
            
        if self.first_click:
            mask = [[0 for _ in range(self.n)] for _ in range(self.n)]
            start_int = random.choice([self.k // 2, self.k // 3])
            bombs_ints = random.sample(range(self.n * self.n), self.k)
            count = 0
            track_masks = [[r, c]]
            track_q = deque([(r ,c)])
            # track_q.append((r, c))
            mask[r][c] = 1
            print("start int", start_int)
            while count <= start_int:
                if not len(track_q):
                    break
                r, c  = track_q.popleft()
                for i, j in self.moves:
                    m, n = r + i, c + j
                    if m < 0 or n < 0 or m == self.n or n == self.n:
                        continue
                    if [m, n] not in track_masks:
                        # if random.choice([True, False]):
                            mask[m][n] = 1
                            track_masks.append([m, n])
                            track_q.extend([(m, n)])
                            count += 1
                            # print(count)
                            print(f"r: {m}, c: {n}, count:{count}")
                    if count >= start_int:
                        break

            for i in range(self.n):
                for j in range(self.n):
                    print(f"{mask[i][j]}  ", end='')
                print()
            print(track_masks)

            bombs_ints.sort()
            for i, idx in enumerate(bombs_ints):
                r, c = divmod(idx, self.n)
                while [r, c] in track_masks and idx in bombs_ints:
                    idx = random.choice(range(i, self.n * self.n))
                    r, c = divmod(idx, self.n)
                    # track_masks.append([r, c])
                bombs_ints[i] = r * self.n + c
            print("Bombs int:", len(bombs_ints))

            for idx in bombs_ints:
                r, c = divmod(idx, self.n)
                self.matrix[r][c] = -1
                track_masks.append([r, c])

                # Update adjacent tiles
                for i in range(max(0, r-1), min(self.n, r+2)):
                    for j in range(max(0, c-1), min(self.n, c+2)):
                        if self.matrix[i][j] != -1:
                            self.matrix[i][j] += 1

            print("Bombs are unique:", len(set(bombs_ints)) == len(bombs_ints))
            self.first_click = False
            for i in range(self.n):
                for j in range(self.n):
                    if self.matrix[i][j] == -1:
                        print("*  ", end='')
                        continue
                    print(f"{self.matrix[i][j]}  ", end='')
                print()
            return self.matrix, self.mask_mat
        return

# Helper to create a sample board
class mine:
    def __init__(self, n, k):
        self.k = k
        self.n = n
        self.mask_mat =  [[0 for _ in range(n)] for _ in range(n)]
        self.matrix =  [[0 for _ in range(n)] for _ in range(n)]

    def generate_sample_game(self):
        bombs_ints = random.sample(range(self.n * self.n), self.k)
        
        for idx in bombs_ints:
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
    # game = mine(n , k)
    # matrix, mask_mat = game.generate_sample_game()
    # for i in range(game.n):
    #     for j in range(game.n):
    #         if matrix[i][j] == -1:
    #             print("*  ", end='')
    #         else:
    #             print(f"{matrix[i][j]}  ", end='')
    #     print()
    # input()
    game = MineGameUI(root, n, k)
    root.mainloop()
