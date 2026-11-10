# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 20:22:36 2026

@author: uni
"""

class State:
    size = 5

    alphabetti_spaghetti = {
        (0,0): "A", (0,1): "B", (0,2): "C", (0,3): "D", (0,4): "E",
        (1,0): "F", (1,1): "G", (1,2): "H", (1,3): "I", (1,4): "J",
        (2,0): "K", (2,1): "L", (2,2): "M", (2,3): "N", (2,4): "O",
        (3,0): "P", (3,1): "Q", (3,2): "R", (3,3): "S", (3,4): "T",
        (4,0): "U", (4,1): "V", (4,2): "W", (4,3): "X", (4,4): "Y"
    }

    spaghetti_alphabetti = {letter: pos for pos, letter in alphabetti_spaghetti.items()}

    # 1.1
    def __init__(self, grid):
        ''' Initialise the hinger game '''
        assert len(grid) == State.size
        assert all(len(row) == State.size for row in grid)

        self.grid = grid

    # 1.2    
    def __str__(self):
        grid_out = []
        for row in self.grid:
            grid_out.append(" ".join(str(x) for x in row))
        return "\n".join(grid_out)

    #1.7    
    @staticmethod
    def pos_to_letter(r, c):
        return State.alphabetti_spaghetti.get((r, c), None)

    @staticmethod
    def letter_to_pos(letter):
        return State.spaghetti_alphabetti.get(str(letter).upper(), None)
    
    def get_adjacent_cells(self, r, c):
        adj = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < State.size and 0 <= nc < State.size:
                    adj.append((nr, nc))
        return adj
    
    def isHinger(self, r , c):
        
        if self.grid[r][c] <=0:
            return False
        
        orig = self.numRegions()
        self.grid[r][c] -= 1
        new_reg = self.numRegions()
        self.grid[r][c] += 1
        return new_reg > orig
    
    # 1.3
    def move(self, mov_letter):
        # 1. Find position using your helper
        pos = State.letter_to_pos(mov_letter)
        if pos is None:
            return False, 0, 0

        r, c = pos

        # 2. Check if target cell has counters (> 0)
        if self.grid[r][c] <= 0:
            return False, 0, 0

        # 3. Next step: Calculate cost, bonus, and remove 1 counter from grid
        
        
    # 1.4 successor generator
    
    def successors(self):
        ''' Yields tuples of (move_letter, new_state_object) '''
        for r in range(State.size):
            for c in range(State.size):
                if self.grid[r][c] > 0:
                    letter = self.alphabetti_spaghetti(r, c)
                    
                    new_grid = [list(row) for row in self.grid]
                    new_grid[r][c] -= 1
                    yield letter, State(new_grid)
    # 1.5                 
    def numRegions(self):
        ''' Calcuates and returns the number of directionally connection active cells'''
        
        visted = set()
        regions = 0 
        
        for r in range(State.size):
            for c in range(State.size):
                if self.grid[r][c] > 0 and (r, c) not in visted:
                    regions += 1
                    stack = [(r, c)]
                    visted.app((r, c))
                    while stack:
                        curr_r, curr_c = stack.pop()
                        for nr, nc in self.get_adjacent_cells(curr_r, curr_c):
                            visted.add((nr, nc))
                            stack.append((nr, nc))
    # 1.6                        
    def numHinger(self):
        ''' returns total number of hinger cells on current board '''
        
        count = 0 
        for r in range(State.size):
            for c in range(State.size):
                if self.grid[r][c] > 0 and self.isHinger(r, c):
                    count += 1
        return count
    
# 1.8 Tester Function
def tester():
    ''' Validates State implementation '''
    print("--- Testing State Class ---")
    s1_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1]
    ]
    sa = State(s1_grid)
    print("State sa (s1):")
    print(sa)
    print("Active regions in sa:", sa.numRegions())
    print("Hingers in sa:", sa.numHingers())


if __name__ == "__main__":
    tester()
