"""The main game logic for our Hinger game."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import time
from hinger_gui import HingerGUI
from scene_manager import Scene
from a1_state import State
from a2_agent import Agent
import random_grid


class HingerGame:

    def __init__(self):
        """Initialise the game controller."""           
        self.initial_state = State(random_grid.generate_grid())
        self.board = None

        self.agentA = None
        self.agentB = None
        self.versus = False
        
        self.scores = [100, 100]
        
        self.turn_time_limit = 60.0
        self.turn_started_at = None
        self.total_time_used = [0.0, 0.0]
        
        self.current_player = 0 #0 = player A, 1  = player B

        self.playing = False
        self.game_over = False
        self.winner = None

        self.move_count = 0
        self.move_history = []
        self.last_move = None
        
        self.ui = HingerGUI(self)
       
    def set_players(self, versus = False):
        """Configure Human vs AI or Agent vs Agent."""
        if versus:
            # Human vs AI
            self.agentA = None
            self.agentB = Agent("Computer")
            self.versus = True

        else:
            # AI vs AI
            self.agentA = Agent("Computer A")
            self.agentB = Agent("Computer B")
            self.versus = False
            
    def begin(self):
        """Prepare a new game."""
        self.board = State(self.initial_state.grid)

        self.scores = [100, 100]
        self.total_time_used = [0.0, 0.0]

        self.current_player = 0

        self.move_count = 0
        self.move_history = []
        self.last_move = None

        self.playing = False
        self.game_over = False
        self.winner = None

        self.play(self.board, self.agentA, self.agentB)
            
    def play(self, state, agentA=None, agentB=None):
        """Start gameplay."""
        self.board = State(state.grid)
        self.agentA = agentA
        self.agentB = agentB

        self.playing = True
        self.start_turn()

        self.ui.scene.change_scene(Scene.GAME)

    def start_turn(self):
        """Start the current player's 60-second timer."""
        self.turn_started_at = time.monotonic()


    def get_turn_time_used(self):
        """Return seconds elapsed during the current turn."""
        if self.turn_started_at is None:
            return 0.0

        return time.monotonic() - self.turn_started_at


    def get_remaining_time(self):
        """Return seconds remaining in the current turn."""
        remaining = self.turn_time_limit - self.get_turn_time_used()

        return max(0.0, remaining)


    def finish_turn(self):
        """Record the current player's time spent on this turn."""

        elapsed = self.get_turn_time_used()

        self.total_time_used[self.current_player] += elapsed

        self.turn_started_at = None


    def update_timer(self):
        """Check whether the current player's time has expired."""

        if not self.playing or self.turn_started_at is None:
            return

        if self.get_remaining_time() <= 0:
            self.finish_turn()
            # Opponent wins
            winner = 1 - self.current_player
            self.end_game(winner)

        def end_game(self, winner=None):
            """Finish the game and determine the winner."""
            # Record the winner or draw.

        def handle_move(self, letter):
            """Validate and execute a player's move."""
            # Update state, score and move history.

        def next_turn(self):
            """Switch between Player A and Player B."""
            self.current_player = 1 - self.current_player

def start():
    game = HingerGame()
    game.ui.run()
   # agent_a = Agent()
   # assert agent_a.name == "B19"
    #assert agent_a.modes == ["minimax", "alphabeta", "mcts"]
   # assert "B19_A" in str(agent_a)
   # assert Agent("Test player A").name == "Test player A"
    
    
   # agent_b = Agent()
   # assert agent_b.name == "B19"
   # assert agent_b.modes == ["minimax", "alphabeta", "mcts"]
   # assert "B19_B" in str(agent_b)
   # assert Agent("Test player B").name == "Test player B"
    

if __name__ == "__main__":
    start()