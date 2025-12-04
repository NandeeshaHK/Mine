from typing import List, Tuple, Set, Dict, Optional
from collections import deque

class MinesweeperSolver:
    def __init__(self):
        pass

    def get_next_move(self, grid_state: List[List[int]], flags_left: int) -> Tuple[Optional[str], Optional[int], Optional[int]]:
        """
        Analyzes the grid state and returns the next best move.
        Returns: (Action, Row, Col) where Action is 'REVEAL', 'FLAG', or None if no sure move.
        """
        n = len(grid_state)
        
        # 1. Basic Rule: If a cell has 'N' flags around it and its number is 'N', all other neighbors are safe.
        # 2. Basic Rule: If a cell has 'N' hidden neighbors and its number is 'N' + existing flags, all hidden neighbors are mines.
        
        # Identify boundary cells (revealed cells with hidden neighbors)
        boundary_cells = []
        for r in range(n):
            for c in range(n):
                if grid_state[r][c] >= 0: # Revealed number
                    neighbors = self._get_neighbors(r, c, n)
                    hidden_neighbors = [(nr, nc) for nr, nc in neighbors if grid_state[nr][nc] == -2]
                    flagged_neighbors = [(nr, nc) for nr, nc in neighbors if grid_state[nr][nc] == -1]
                    
                    if not hidden_neighbors:
                        continue
                        
                    # Rule 2: All neighbors are mines
                    if grid_state[r][c] == len(hidden_neighbors) + len(flagged_neighbors):
                        return 'FLAG', hidden_neighbors[0][0], hidden_neighbors[0][1]
                    
                    # Rule 1: All neighbors are safe
                    if grid_state[r][c] == len(flagged_neighbors):
                         return 'REVEAL', hidden_neighbors[0][0], hidden_neighbors[0][1]
                    
                    boundary_cells.append((r, c))

        # TODO: Advanced CSP/Backtracking logic could go here if basic rules fail.
        # For now, if no safe move is found, we can return None or implement a probability-based guess.
        
        return None, None, None

    def _get_neighbors(self, r: int, c: int, n: int) -> List[Tuple[int, int]]:
        neighbors = []
        for i in range(max(0, r - 1), min(n, r + 2)):
            for j in range(max(0, c - 1), min(n, c + 2)):
                if i == r and j == c:
                    continue
                neighbors.append((i, j))
        return neighbors
