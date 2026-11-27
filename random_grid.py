# -*- coding: utf-8 -*-
"""
Random grid generator to initialise state
"""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William


import random
from a1_state import State

GRID_SIZE = 5


def generate_grid():
    """Generate a random 5x5 grid containing at least 3 hingers."""

    while True:

        # Generate a random board
        grid = [
            [random.randint(0, 1) for _ in range(GRID_SIZE)]
            for _ in range(GRID_SIZE)
        ]

        # Count the hingers on the board
        state = State(grid)
        hingers = state.numHingers()

        # Only accept boards containing at least 3 hingers
        if hingers >= 3:
            return grid


def tester():
    """Test random grid generation."""

    generated = []

    for _ in range(100):
        grid = generate_grid()

        # Grid must contain exactly 5 rows.
        assert len(grid) == GRID_SIZE

        # Every row must contain exactly 5 cells.
        assert all(len(row) == GRID_SIZE for row in grid)

        # Every cell must contain either 0 or 1.
        assert all(
            cell in (0, 1)
            for row in grid
            for cell in row
        )

        # There must be at least one active cell.
        assert any(
            cell == 1
            for row in grid
            for cell in row
        )
        
        # Every generated board must contain at least 3 hingers
        assert State(grid).numHingers() >= 3

        generated.append(tuple(tuple(row) for row in grid))

    # Check that generation produces different boards.
    assert len(set(generated)) > 1

    print("random_grid tester: PASS")


if __name__ == "__main__":
    tester()

    print("\nExample generated grid:")

    for row in generate_grid():
        print(row)
