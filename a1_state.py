# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 19:30:12 2026

@author: seane
"""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William


class State:
    size = 5

    def __init__(self, grid):
        """Create a state from a 5 × 5 grid."""

        # Check that the grid has five rows.
        assert len(grid) == State.size

        # Check that every row has five cells.
        for row in grid:
            assert len(row) == State.size

            # Each cell must be empty or contain one counter.
            for cell in row:
                assert cell in (0, 1)

        # Copy the rows so the state owns its own board.
        self.grid = [row[:] for row in grid]

    def __str__(self):
        """Return the board as readable rows of numbers."""
        rows = []

        for row in self.grid:
            line = " ".join(str(cell) for cell in row)
            rows.append(line)

        return "\n".join(rows)
    
    def move(self, letter):
        """Return (moved, was_hinger)."""

        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXY" or len(letter) != 1:
            return False, False

        index = ord(letter) - ord("A")
        row = index // 5  # Whole-number division gives the row.
        col = index % 5   # Remainder gives the column.

        if self.grid[row][col] == 0:
            return False, False

        regions_before = self.numRegions()

        # Remove the counter.
        self.grid[row][col] = 0

        regions_after = self.numRegions()

        was_hinger = regions_after > regions_before

        return True, was_hinger

    def numRegions(self):
        """Count connected groups of counters, including diagonals."""

        visited = set()
        regions = 0

        for row in range(State.size):
            for col in range(State.size):

                # Skip empty cells and counters already counted.
                if self.grid[row][col] == 0:
                    continue

                if (row, col) in visited:
                    continue

                # This counter belongs to a new region.
                regions += 1
                stack = [(row, col)]
                visited.add((row, col))

                # Find all counters connected to this one.
                while stack:
                    current_row, current_col = stack.pop()
                    
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):

                            # A cell is not its own neighbour.
                            if dr == 0 and dc == 0:
                                continue

                            next_row = current_row + dr
                            next_col = current_col + dc

                            # Stay within the board.
                            if not (0 <= next_row < State.size):
                                continue

                            if not (0 <= next_col < State.size):
                                continue
                            
                            position = (next_row, next_col)

                            if (self.grid[next_row][next_col] == 1
                                    and position not in visited):
                                visited.add(position)
                                stack.append(position)

        return regions
    
    def numHingers(self):
        """Return the number of hinger cells on the board."""

        hingers = 0
        regions_before = self.numRegions()

        for row in range(State.size):
            for col in range(State.size):

                # Only cells containing a counter can be hingers.
                if self.grid[row][col] == 1:

                    # Create an independent copy of the board.
                    copied_grid = [r[:] for r in self.grid]
                    test_state = State(copied_grid)

                    # Remove this counter from the copy.
                    test_state.grid[row][col] = 0

                    # A hinger's removal increases the region count.
                    if test_state.numRegions() > regions_before:
                        hingers += 1
        return hingers
    
    def successors(self):
        """Yield every state reachable by removing one counter."""

        for row in range(State.size):
            for col in range(State.size):

                if self.grid[row][col] == 1:

                    # Create an independent copy of the board.
                    copied_grid = [r[:] for r in self.grid]
                    next_state = State(copied_grid)

                    # Remove one counter from the copy.
                    next_state.grid[row][col] = 0

                    yield next_state
                    
    def get_valid_moves(self, state):
        """Return the letters of cells containing counters."""
        moves = []

        for row in range(State.size):
            for col in range(State.size):
                if state.grid[row][col] == 1:
                    letter = chr(ord("A") + row * State.size + col)
                    moves.append(letter)

        return moves

    def simulate_move(self, state, letter):
        """Return a new state and the points gained by a legal move."""
        index = ord(letter) - ord("A")
        row = index // State.size
        col = index % State.size

        # Count active neighbours before removing the counter.
        cost = 0

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue

                neighbour_row = row + dr
                neighbour_col = col + dc

                if (0 <= neighbour_row < State.size
                        and 0 <= neighbour_col < State.size):
                    cost += state.grid[neighbour_row][neighbour_col]

        new_state = State(state.grid)
        moved, was_hinger = new_state.move(letter)

        bonus = 100 if was_hinger else 0
        points = bonus - cost

        return new_state, points

                    
def tester():
    grid = [
        [1, 0, 0, 0, 1],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    # 1. Creating and printing a state.
    practice = State(grid)
    print(practice)
    expected = "1 0 0 0 1\n0 1 0 0 0\n0 0 1 0 0\n0 0 0 1 0\n0 0 0 0 0"
    assert str(practice) == expected, "Incorrect board display"

    # Changing the input list must not change the state.
    grid[0][0] = 0
    assert practice.grid[0][0] == 1, "The board was not copied"
    grid[0][0] = 1

    # 2. Diagonal connections and hingers.
    # The diagonal chain is one region; the top-right counter is another.
    assert practice.numRegions() == 2, "Expected two regions"
    # The two middle counters in the diagonal chain are hingers.
    assert practice.numHingers() == 2, "Expected two hingers"
    assert practice.grid == grid, "Counting changed the board"

    # 3. A legal move that removes a hinger: G is (1, 1).
    state = State(grid)
    assert state.move("G") == (True, True), "G should be a hinger"
    assert state.grid[1][1] == 0, "G was not removed"
    assert state.numRegions() == 3, "Removing G should leave three regions"
    assert state.move("G") == (False, False), "An empty cell is invalid"

    # 4. A legal move that does not remove a hinger.
    state = State(grid)
    assert state.move("A") == (True, False), "A is not a hinger"
    assert state.grid[0][0] == 0

    # 5. Invalid letters must leave the board unchanged.
    state = State(grid)
    for letter in ["Z", "a", "", "AA", "1", "?"]:
        assert state.move(letter) == (False, False), "Invalid letter accepted"
        assert state.grid == grid, "An invalid move changed the board"

    # 6. Check letter mapping at the last cell.
    full_grid = [[1 for col in range(5)] for row in range(5)]
    state = State(full_grid)
    assert state.move("Y") == (True, False)
    assert state.grid[4][4] == 0, "Y should remove the bottom-right counter"
    assert sum(sum(row) for row in state.grid) == 24

    # 7. An empty board has no regions, hingers or successors.
    empty_grid = [[0 for col in range(5)] for row in range(5)]
    empty = State(empty_grid)
    assert empty.numRegions() == 0
    assert empty.numHingers() == 0
    assert list(empty.successors()) == []
    assert empty.move("A") == (False, False)

    # 8. Removing a lone counter does not make it a hinger.
    single_grid = [row[:] for row in empty_grid]
    single_grid[2][2] = 1
    single = State(single_grid)
    assert single.numRegions() == 1
    assert single.numHingers() == 0
    assert single.move("M") == (True, False)
    assert single.numRegions() == 0

    # 9. Each successor must remove exactly one different counter.
    original = State(grid)
    next_states = list(original.successors())
    assert len(next_states) == 5, "Five counters should give five successors"
    removed_positions = set()

    for next_state in next_states:
        differences = []
        for row in range(5):
            for col in range(5):
                if original.grid[row][col] != next_state.grid[row][col]:
                    differences.append((row, col))

        assert len(differences) == 1, "A successor must change exactly one cell"
        row, col = differences[0]
        assert original.grid[row][col] == 1
        assert next_state.grid[row][col] == 0
        removed_positions.add((row, col))

    assert len(removed_positions) == 5, "Successors should not be duplicates"
    assert original.grid == grid, "Generating successors changed the original"

    # Changing one successor must not change another or the original.
    other_before = [row[:] for row in next_states[1].grid]
    next_states[0].grid[4][4] = 1
    assert next_states[1].grid == other_before
    assert original.grid == grid

    # 10. Incorrect board dimensions and values must be rejected.
    bad_value = [row[:] for row in grid]
    bad_value[0][0] = 2
    bad_width = [row[:] for row in grid]
    bad_width[2] = [0, 0]

    for invalid_grid in [grid[:4], bad_width, bad_value]:
        try:
            State(invalid_grid)
        except AssertionError:
            pass
        else:
            raise AssertionError("An invalid grid was accepted")

    print("All additional tests passed.")


if __name__ == "__main__":
    tester()