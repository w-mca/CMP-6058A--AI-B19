"""The main game logic for our Hinger game."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
from hinger_gui import HingerGUI
from a1_state import State
from a2_agent import Agent


class HingerGame:

    def __init__(self):
        """Initialise the game controller."""       
        
        self.board = None
        self.initial_state = None

        self.agentA = None
        self.agentB = None
        self.versus = False

        self.playing = False
        self.game_over = False
        self.winner = None

        self.current_player = 0 #0 = player A, 1  = player B
        self.scores = [100, 100]

        self.move_count = 0
        self.move_history = []
        self.last_move = None
        
        self.ui = HingerGUI(self)
        self.ui.run()

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

    def play(self, state, agentA=None, agentB=None):
        """Start a new game."""
        self.board = State(state.grid)
        self.initial_state = State(state.grid)
        self.agentA = agentA
        self.agentB = agentB
        # Reset the board, scores and player turns.

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