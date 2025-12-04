import random
from typing import List, Tuple, Set, Optional

class MinesweeperGame:
    def __init__(self, n: int, k: int):
        self.n = n  # Grid size (n x n)
        self.k = k  # Number of mines
        self.grid = [[0 for _ in range(n)] for _ in range(n)]
        self.mask = [[-2 for _ in range(n)] for _ in range(n)] # -2: Hidden, -1: Flagged, >=0: Revealed
        self.flags_left = k
        self.game_over = False
        self.won = False
        self.first_click = True
        self.mines_loc: Set[Tuple[int, int]] = set()

    def _get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        neighbors = []
        for i in range(max(0, r - 1), min(self.n, r + 2)):
            for j in range(max(0, c - 1), min(self.n, c + 2)):
                if i == r and j == c:
                    continue
                neighbors.append((i, j))
        return neighbors

    def _place_mines(self, safe_r: int, safe_c: int):
        # Ensure the first click and its neighbors are safe
        safe_zone = set(self._get_neighbors(safe_r, safe_c))
        safe_zone.add((safe_r, safe_c))

        available_cells = [
            (r, c) for r in range(self.n) for c in range(self.n)
            if (r, c) not in safe_zone
        ]
        
        if len(available_cells) < self.k:
             # Fallback if k is too large (shouldn't happen with reasonable defaults)
             available_cells = [(r, c) for r in range(self.n) for c in range(self.n) if (r,c) != (safe_r, safe_c)]

        self.mines_loc = set(random.sample(available_cells, self.k))

        for r, c in self.mines_loc:
            self.grid[r][c] = -1 # -1 represents a mine

        # Calculate numbers
        for r in range(self.n):
            for c in range(self.n):
                if self.grid[r][c] == -1:
                    continue
                count = 0
                for nr, nc in self._get_neighbors(r, c):
                    if self.grid[nr][nc] == -1:
                        count += 1
                self.grid[r][c] = count

    def reveal(self, r: int, c: int) -> bool:
        """
        Returns True if the move was safe, False if a mine was hit.
        """
        if self.game_over or self.mask[r][c] == -1: # Ignore if game over or flagged
            return True

        if self.first_click:
            self._place_mines(r, c)
            self.first_click = False

        if self.grid[r][c] == -1:
            self.game_over = True
            self.won = False
            self.mask[r][c] = -1 # Show the mine
            return False

        # BFS for flood fill
        queue = [(r, c)]
        visited = set()
        
        while queue:
            curr_r, curr_c = queue.pop(0)
            if (curr_r, curr_c) in visited:
                continue
            visited.add((curr_r, curr_c))
            
            if self.mask[curr_r][curr_c] == -1: # Don't reveal flagged cells automatically
                 continue

            self.mask[curr_r][curr_c] = self.grid[curr_r][curr_c]

            if self.grid[curr_r][curr_c] == 0:
                for nr, nc in self._get_neighbors(curr_r, curr_c):
                    if self.mask[nr][nc] == -2:
                        queue.append((nr, nc))
        
        self._check_win()
        return True

    def toggle_flag(self, r: int, c: int):
        if self.game_over:
            return

        if self.mask[r][c] == -2: # Hidden
            if self.flags_left > 0:
                self.mask[r][c] = -1
                self.flags_left -= 1
        elif self.mask[r][c] == -1: # Flagged
            self.mask[r][c] = -2
            self.flags_left += 1
            
    def _check_win(self):
        # Win condition: All non-mine cells are revealed
        revealed_count = sum(1 for r in range(self.n) for c in range(self.n) if self.mask[r][c] >= 0)
        if revealed_count == (self.n * self.n) - self.k:
            self.game_over = True
            self.won = True
            # Flag all mines
            for r, c in self.mines_loc:
                self.mask[r][c] = -1
            self.flags_left = 0

    def get_state(self):
        return self.mask
