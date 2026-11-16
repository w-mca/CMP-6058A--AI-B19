"""An agent for the Hinger game."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import math
import random
import a1_state as state
class Agent:
    """Represent a Hinger player and its available strategy modes."""

    def __init__(self, name: str = "B19"):
        """Initialise the agent with its name and supported strategies."""
        self.name = name
        self.modes = ["minimax","alphabeta","mcts"]
        self.moving = False
        self.strategy = None

    def __str__(self):
        return f"Agent {self.name} (modes: {', '.join(self.modes)})"

    def get_valid_moves(self, board):
        return board.get_valid_moves(board)

    def simulate_move(self, board, letter):
        return board.simulate_move(board, letter)

    def next_move(self, state):
        """Return a move using the chosen strategy."""

        # No counters means no move is possible.
        if not any(1 in row for row in state.grid):
            return None

        if self.strategy == "minimax":
            return self.minimax_move(state)
        elif self.strategy == "alphabeta":
            return self.alphabeta_move(state)
        elif self.strategy == "mcts":
            return self.mcts_move(state)   
        else:
            raise ValueError("Unknown playing mode")
        return f"Agent {self.name} (modes: {', '.join(self.modes)})"
    
    def minimax_move(self, state, depth=3):
        """Return the best move using depth-limited minimax."""
        if depth < 1:
            raise ValueError("Depth must be at least 1")

        best_score = float("-inf")
        best_move = None

        for letter in self.get_valid_moves(state):
            new_state, points, was_hinger = self.simulate_move(state, letter)

            # The opponent plays next, so is_maximizing is False.
            score = self.minimax(
                new_state,
                False,
                depth - 1,
                points
                )

            if score > best_score:
                best_score = score
                best_move = letter
                best_was_hinger = was_hinger

        return best_move, best_was_hinger
    
    def minimax(self, state, is_maximizing, depth, score_difference):
        """Evaluate future moves from this agent's perspective."""
        moves = self.get_valid_moves(state)

        if depth == 0 or not moves:
            return score_difference

        if is_maximizing:
            best_score = float("-inf")

            for letter in moves:
                new_state, points, was_hinger = self.simulate_move(state, letter)

                score = self.minimax(
                    new_state,
                    False,
                    depth - 1,
                    score_difference + points
                    )

                best_score = max(best_score, score)

            return best_score

        else:
            best_score = float("inf")

            for letter in moves:
                new_state, points, was_hinger = self.simulate_move(state, letter)

                score = self.minimax(
                    new_state,
                    True,
                    depth - 1,
                    score_difference - points
                    )

                best_score = min(best_score, score)

            return best_score
        
    def alphabeta_move(self, state, depth=3):
        """Return the best move using alpha-beta pruning."""
        if depth < 1:
            raise ValueError("Depth must be at least 1")

        best_score = float("-inf")
        best_move = None

        alpha = float("-inf")
        beta = float("inf")

        for letter in self.get_valid_moves(state):
            new_state, points, was_hinger = self.simulate_move(state, letter)

            score = self.alphabeta(
                new_state,
                False,
                depth - 1,
                points,
                alpha,
                beta
                )

            if score > best_score:
                best_score = score
                best_move = letter
                best_was_hinger = was_hinger

            alpha = max(alpha, best_score)

        return best_move, best_was_hinger
    
    def alphabeta(self, state, is_maximizing, depth,
                  score_difference, alpha, beta):
        """Evaluate future moves, pruning unnecessary branches."""
        moves = self.get_valid_moves(state)

        if depth == 0 or not moves:
            return score_difference

        if is_maximizing:
            best_score = float("-inf")

            for letter in moves:
                new_state, points, was_hinger = self.simulate_move(state, letter)

                score = self.alphabeta(
                    new_state,
                    False,
                    depth - 1,
                    score_difference + points,
                    alpha,
                    beta
                    )

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

            return best_score

        else:
            best_score = float("inf")

            for letter in moves:
                new_state, points, was_hinger = self.simulate_move(state, letter)

                score = self.alphabeta(
                    new_state,
                    True,
                    depth - 1,
                    score_difference - points,
                    alpha,
                    beta
                    )
                
                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

            return best_score
        
    def mcts_move(self, board, iterations=1000, seed=None):
        """Choose a move using Monte Carlo Tree Search."""
        if iterations < 1:
            raise ValueError("Iterations must be at least 1")

        rng = random.Random(seed)

        # Each node stores a board and its search statistics.
        def make_node(board, maximizing, letter=None):
            return {
                "state": board,
                "maximizing": maximizing,
                "letter": letter,
                "untried": self.get_valid_moves(board),
                "children": [],
                "visits": 0,
                "total_reward": 0.0
                }

        root = make_node(state.State(board.grid), True)

        if not root["untried"]:
            return None

        # Keep the reward between -1 and 1.
        # Each remaining move changes the score by at most 100.
        reward_scale = 100 * len(root["untried"])

        for iteration in range(iterations):
            node = root
            path = [node]
            score_difference = 0

            # 1. SELECTION
            # Follow existing branches until expansion is possible.
            while not node["untried"] and node["children"]:
                
                def uct(child):
                    average = (
                        child["total_reward"] / child["visits"]
                        )

                    # Opponent turns favour lower scores for us.
                    if not node["maximizing"]:
                        average = -average

                    exploration = math.sqrt(
                        2 * math.log(node["visits"])
                        / child["visits"]
                        )

                    return average + exploration

                child = max(node["children"], key=uct)

                new_state, points, was_hinger = self.simulate_move(
                    node["state"], child["letter"]
                    )

                if node["maximizing"]:
                    score_difference += points
                else:
                    score_difference -= points

                node = child
                path.append(node)

            # 2. EXPANSION
            # Add one previously unexplored move.
            if node["untried"]:
                letter = rng.choice(node["untried"])
                node["untried"].remove(letter)

                new_state, points, was_hinger = self.simulate_move(
                    node["state"], letter
                    )

                if node["maximizing"]:
                    score_difference += points
                else:
                    score_difference -= points

                child = make_node(
                    new_state,
                    not node["maximizing"],
                    letter
                    )

                node["children"].append(child)
                node = child
                path.append(node)

            # 3. SIMULATION
            # Play random moves until the board is empty.
            rollout_state = state.State(node["state"].grid)
            maximizing = node["maximizing"]
            moves = self.get_valid_moves(rollout_state)

            while moves:
                letter = rng.choice(moves)

                rollout_state, points, was_hinger = self.simulate_move(
                    rollout_state, letter
                    )

                if maximizing:
                    score_difference += points
                else:
                    score_difference -= points

                maximizing = not maximizing
                moves = self.get_valid_moves(rollout_state)

            # 4. BACKPROPAGATION
            # Update every node visited during this iteration.
            reward = score_difference / reward_scale

            for visited_node in path:
                visited_node["visits"] += 1
                visited_node["total_reward"] += reward

        # Choose the move explored most often.
        best_child = max(
            root["children"],
            key=lambda child: child["visits"]
            )
        
        best_move = best_child["letter"]
        # Check whether the chosen move is a hinger on the original board.
        _, _, was_hinger = self.simulate_move(board, best_move)
        
        return best_child["letter"], was_hinger


def tester():
    """Test Minimax, Alpha-Beta and MCTS agents."""
    agent = Agent()

    assert agent.name == "B19"
    assert agent.modes == ["minimax", "alphabeta", "mcts"]
    assert "B19" in str(agent)
    print(agent)

    # 1. EMPTY BOARD
    empty_grid = [[0] * 5 for _ in range(5)]
    empty = state.State(empty_grid)

    for mode in agent.modes:
        agent.strategy = mode
        assert agent.next_move(empty) is None

    assert agent.get_valid_moves(empty) == []
    print("PASS: Empty board")

    # 2. SINGLE AVAILABLE MOVE
    single_grid = [row[:] for row in empty_grid]
    single_grid[4][4] = 1
    single = state.State(single_grid)

    for mode in agent.modes:
        agent.strategy = mode
        letter, was_hinger = agent.next_move(single)
        assert letter == "Y"
        assert isinstance(was_hinger, bool)
        assert single.grid == single_grid

    print("PASS: Single available move")

    # 3. SIMULATE MOVE
    chain_grid = [row[:] for row in empty_grid]
    chain_grid[2][0:3] = [1, 1, 1]
    chain = state.State(chain_grid)

    assert agent.get_valid_moves(chain) == ["K", "L", "M"]

    after, points, was_hinger = agent.simulate_move(chain, "L")

    assert points == 98
    assert was_hinger is True
    assert after.grid[2][1] == 0
    assert after.numRegions() == 2
    assert chain.grid == chain_grid

    after, points, was_hinger = agent.simulate_move(chain, "K")

    assert points == -1
    assert was_hinger is False
    assert after.grid[2][0] == 0
    assert chain.grid == chain_grid

    print("PASS: Move simulation and hinger detection")

    # 4. MINIMAX AND ALPHA-BETA
    for depth in (1, 2, 3):
        assert agent.minimax_move(chain, depth) == ("L", True)
        assert agent.alphabeta_move(chain, depth) == ("L", True)

    mm_score = agent.minimax(chain, True, 3, 0)

    ab_score = agent.alphabeta(
        chain, True, 3, 0,
        float("-inf"), float("inf")
    )

    assert mm_score == ab_score == 98

    print("PASS: Minimax and Alpha-Beta choose the hinger")

    # 5. COMPARE MINIMAX AND ALPHA-BETA
    corner_grid = [row[:] for row in empty_grid]

    for row, col in [(0, 0), (0, 4), (4, 0), (4, 4)]:
        corner_grid[row][col] = 1

    diagonal_grid = [row[:] for row in empty_grid]

    for row, col in [(0, 0), (1, 1), (2, 2), (3, 3)]:
        diagonal_grid[row][col] = 1

    for grid in [chain_grid, corner_grid, diagonal_grid]:
        board = state.State(grid)

        for depth in (1, 2, 3, 4):
            assert (
                agent.minimax_move(board, depth)
                == agent.alphabeta_move(board, depth)
            )

            for maximizing in (True, False):
                mm = agent.minimax(board, maximizing, depth, 7)

                ab = agent.alphabeta(
                    board, maximizing, depth, 7,
                    float("-inf"), float("inf")
                )

                assert mm == ab

        assert board.grid == grid

    print("PASS: Minimax and Alpha-Beta agree")

    # 6. MCTS
    first = agent.mcts_move(chain, iterations=300, seed=2026)
    second = agent.mcts_move(chain, iterations=300, seed=2026)

    assert first == second
    assert first[0] in agent.get_valid_moves(chain)
    assert first == ("L", True)
    assert chain.grid == chain_grid

    print("PASS: MCTS is repeatable and finds the hinger")

    # 7. NEXT_MOVE DISPATCHER
    for mode in agent.modes:
        agent.strategy = mode

        result = agent.next_move(chain)
        letter, was_hinger = result

        assert letter in agent.get_valid_moves(chain)

        _, _, expected_hinger = agent.simulate_move(chain, letter)

        assert was_hinger == expected_hinger
        assert chain.grid == chain_grid

        print(f"PASS: {mode} chose {letter}, hinger={was_hinger}")

    # 8. UNKNOWN STRATEGY
    agent.strategy = "unknown"

    try:
        agent.next_move(chain)
    except ValueError:
        pass
    else:
        raise AssertionError("Unknown strategy should raise ValueError")

    print("PASS: Unknown strategy rejected")

    # 9. INVALID SEARCH DEPTH
    for search in [agent.minimax_move, agent.alphabeta_move]:
        try:
            search(chain, depth=0)
        except ValueError:
            pass
        else:
            raise AssertionError("Depth zero should be rejected")

    print("PASS: Invalid search depth rejected")

    # 10. INVALID MCTS ITERATIONS
    try:
        agent.mcts_move(chain, iterations=0)
    except ValueError:
        pass
    else:
        raise AssertionError("Zero iterations should be rejected")

    print("PASS: Invalid MCTS iterations rejected")

    print("\nALL AGENT TESTS PASSED!")


if __name__ == "__main__":
    tester()

    
if __name__ == "__main__":
    tester()