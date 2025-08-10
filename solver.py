from gui import MineGameUI
from collections import deque, defaultdict
import tkinter as tk
import random
import time
import heapq

class solver:
    def __init__(self, n, k):
        self.root = tk.Tk()
        self.n = n
        self.k = k
        self.first_click = True

        # Solver Variables
        self.graph = defaultdict(list)
        self.min_heap = []
        self.done = set()
        self.bombs = set()

        # Initialize the Game Engine, and read the state Matrix pointer
        self.obj = MineGameUI(self.root, n, k)
        self.state = self.obj.state_mat 
        self.moves = self.obj.moves
        self.first_random()

    def click(self, r, c):
        self.done.add(r * self.n + c)
        self.obj.left_click(r, c)

    def flag(self, r, c):
        self.obj.right_click(r, c)
        self.state[r][c] = -1
        self.bombs.add(r * self.n + c)

    def get_cell_state(self, r, c):
        count = 0
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.state[i][j] == -2:
                    count += 1
        if count == 0:
            self.done.add(r * self.n + c)
        
        if self.state[r][c] == count:
            self.click(r, c)
        return count, self.state[r][c] == count

    def mark_flags_for_solvable(self, r, c, count):
        count_flagged = 0
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.state[i][j] == -1:
                    count_flagged += 1
                if self.state[i][j] == -2 and count != 0:
                    self.flag(i, j)
                    count -= 1
                    self.flag(i, j)

    def click_if_all_bombs_flagged(self, r, c):
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.state[i][j] == -2 and count != 0:
                    self.flag(i, j)
                    count -= 1

    def is_all_discovered_cell(self, idx=None, r=None, c=None):
        if idx:
            r, c = divmod(idx, self.n)
        
        if r != None:
            count = 0
            for i in range(max(0, r-1), min(self.n, r+2)):
                for j in range(max(0, c-1), min(self.n, c+2)):
                    count 


    def solve(self):

        for idx in self.done:
            r, c = divmod(idx, self.n)

            count, solvable= self.get_cell_state(r, c)

    # Call this only once, for initial reading
    def read_state(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.state[i][j] != -2:
                    idx = i * self.n + j
                    self.done.add(idx)
                    count, solvable, all_nodes_explored = self.get_cell_state(i, j)


    def first_random(self):
        if self.first_click:
            r, c = divmod(random.randint(0, self.n * self.n), self.n)
            self.first_click = False
            self.click(r, c)
        

        
if __name__ == "__main__":
    solve = solver(16, 40)
    solve.root.mainloop()
    