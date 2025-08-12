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
        self.que = deque()
        self.done = set()
        self.coast = set()
        self.bombs = set()

        # Initialize the Game Engine, and read the state Matrix pointer
        self.obj = MineGameUI(self.root, n, k)
        self.state = self.obj.state_mat 
        self.moves = self.obj.moves
        self.game_over = self.obj.game_over
        # self.obj.root.after(1000)
        self.first_random()

    def click(self, r, c):
        if r * self.n + c not in self.done:
            # self.done.add(r * self.n + c)
            check = self.obj.left_click(r, c)
            self.state = self.obj.state_mat
            return check
        # self.obj.root.after(1000)
        
    def flag(self, r, c):
        self.obj.right_click(r, c)
        self.state[r][c] = -1
        self.bombs.add(r * self.n + c)
        self.obj.root.after(1000)
        self.debug()

    def debug(self, r=None, c=None):
        with open('state.txt', mode="w") as file:       
            for i in range(self.n):
                string = ''
                for j in range(self.n):
                    if self.state[i][j] == -2:
                        string += 'X  '
                    elif self.state[i][j] == -1:
                        string += 'B  '
                    elif r == i and c == j: 
                        string += str(self.state[i][j]) + '< '
                    else: 
                        string += str(self.state[i][j]) + '  '  # ensure it's string
                file.write(string + "\n")  # write row and move to next line
    
    def bfs(self, i, j):
        heapq.heappush(self.min_heap, (0, i * self.n + j))
        self.coast.add(i * self.n + j)
        self.que.append(i * self.n + j)
        while self.que:
                idx = self.que.popleft()
                # _, idx = heapq.heappop(self.min_heap)
                r, c = divmod(idx, self.n)
                # print(self.min_heap)

                if idx not in self.done:
                    count, solvable = self.update_cell_state(r, c)
                
                self.debug()

                if len(self.bombs) + len(self.done) == self.n * self.n:
                    print("Solved the MineSweeper")
                    for i in range(self.n):
                        for j in range(self.n):
                            if self.state[i][j] != -1:
                                print(f'*  ', end='')
                            else: 
                                print(f'{self.state[i][j]}  ', end='')
                        print()
                
                if idx in self.done:
                    try:
                        self.coast.remove(idx)
                    except:
                        pass
                
                if len(self.coast) < 2:
                    print("Not enough clues to search for a Solution ... Exiting ...")
                    exit(1)
              
            
    def update_cell_state(self, r, c):
        if self.game_over:
            print("Exiting the game solving ....")
            exit(0)
        count = 0
        count_flagged = 0
        node_dict = defaultdict(list)
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.state[i][j] == -2:
                    count += 1
                    node_dict[-2].append((i, j))
                elif self.state[i][j] == -1:
                    count_flagged += 1
                    # node_dict[-1].append((i, j))
                else:
                    idx = i * self.n + j
                    if idx not in self.done:
                        # self.que.ap(idx)
                        # heapq.heappush(self.min_heap, (self.state[i][j], idx))
                        self.coast.add(idx)
                        self.que.append(idx)
                        # co, sol = self.update_cell_state(i, j)
        # when bombs flagged count + unexplored cells count = cell_count
        # click on all unexplored
        idx  = r * self.n + c

        if count + count_flagged == self.state[r][c]:
            for i, j in node_dict[-2]:
                self.flag(i, j)
            try:
                self.coast.remove(idx)
            except KeyError as e:
                print(f"{idx} was never added in the Coast set")
            self.done.add(idx)

        check = False
        while count != 0 and count_flagged == self.state[r][c] and not check:
            check = self.click(r, c)
            self.done.add(idx)

        if count == 0:
            try:
                self.coast.remove(idx)
            except KeyError as e:
                print(f"{idx} doesn't exists no longer in the Coast set")
            self.done.add(idx)
        
        if self.state[r][c] == count:
            time.sleep(0.2)
            self.click(r, c)
            
        if count > self.state[r][c] - count_flagged:
            self.coast.add(idx)
            self.que.append(idx)
            # heapq.heappush(self.min_heap, (self.state[r][c] - count_flagged, idx))
        
        return count, self.state[r][c] == count

    def click_if_all_bombs_flagged(self, r, c):
        for i in range(max(0, r-1), min(self.n, r+2)):
            for j in range(max(0, c-1), min(self.n, c+2)):
                if self.state[i][j] == -2 and count != 0:
                    self.flag(i, j)
                    count -= 1

    # Call this only once, for initial reading
    def read_state(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.state[i][j] != -2:
                    idx = i * self.n + j
                    self.done.add(idx)
                    count, solvable = self.update_cell_state(i, j)


    def first_random(self):
        if self.first_click:
            r, c = divmod(random.randint(0, self.n * self.n), self.n)
            self.first_click = False
            self.click(r, c)
        if self.game_over:
            print("Exiting the game solving ....")
            exit(0)
        # if not self.game_over:
        self.bfs(r, c)
        

        
if __name__ == "__main__":
    import sys
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(10000)
    print(sys.getrecursionlimit())
    solve = solver(16, 40)
    solve.root.mainloop()
    