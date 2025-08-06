
class Mine:
    def __init__(self, n):
        '''
        n: It is the number of squares in the game
        '''
        self.n = n
        self.matrix = [[ 0 for _ in range(self.n)] for _ in range(self.n)]
        self.mask = [[ 0 for _ in range(self.n)] for _ in range(self.n)]
        pass

    def random_assign(self, k):
        '''
        k: is the number of mines to be assigned
        '''
        import random
        
        visit = set()
        for _ in range(k):
            while len(visit) < k:
                i = random.randint(0, self.n-1)
                j = random.randint(0, self.n-1)
                if (i, j) not in visit:
                    visit.add((i, j))
                    self.matrix[i][j] = -1

    def assign_neighbours(self):
        iter_rc = {-1, 0, 1}
        for i in range(self.n):
            for j in range(self.n):
                if self.matrix[i][j] == -1:
                    for r in iter_rc:
                        for c in iter_rc:
                            if not (r == 0 and c == 0):
                                n_r = i - r
                                n_c = j - c                            
                                if n_c > -1 and n_r > -1:
                                    if n_c < self.n and n_r < self.n and self.matrix[n_r][n_c] != -1:
                                        self.matrix[n_r][n_c] += 1

if __name__ == "__main__":
    game = Mine(16)

    Mine.random_assign(game, k=40)
    Mine.assign_neighbours(game)
    for i in range(game.n):
        for j in range(game.n):
            if game.matrix[i][j] == -1:
                print("*  ", end='')
            else:
                print(f"{game.matrix[i][j]}  ", end='')
        print()