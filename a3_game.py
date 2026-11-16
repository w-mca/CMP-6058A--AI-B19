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
        
        self.turn_time_limit = 10.0 #20
        self.timer_paused_at = None
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
        self.timer_paused_at = None
        self.turn_started_at = time.monotonic()

    
    def get_turn_time_used(self):
        """Return seconds elapsed during the current turn."""
        if self.turn_started_at is None:
            return 0.0
    
        if self.timer_paused_at is not None:
            return self.timer_paused_at - self.turn_started_at
    
        return time.monotonic() - self.turn_started_at


    def get_remaining_time(self):
        """Return seconds remaining in the current turn."""
        remaining = self.turn_time_limit - self.get_turn_time_used()

        return max(0.0, remaining)
    
    def pause_timer(self):
        """Pause the current turn timer."""
        if self.playing and self.turn_started_at is not None:
            if self.timer_paused_at is None:
                self.timer_paused_at = time.monotonic()


    def resume_timer(self):
        """Resume the current turn timer."""
        if self.timer_paused_at is not None:
            if self.turn_started_at is not None:
                paused_duration = time.monotonic() - self.timer_paused_at
                self.turn_started_at += paused_duration
    
            self.timer_paused_at = None


    def finish_turn(self):
        """Record the current player's time spent on this turn."""

        elapsed = self.get_turn_time_used()

        self.total_time_used[self.current_player] += elapsed

        self.turn_started_at = None
        
        # Reset the current AI agent's moving state
        agent = self.agentA if self.current_player == 0 else self.agentB

        if agent is not None:
            agent.moving = False



    def update_timer(self):
        """Check whether the current player's time has expired."""
    
        if not self.playing or self.turn_started_at is None:
            return
    
        if self.timer_paused_at is not None:
            return
    
        if self.get_remaining_time() <= 0:
            self.next_turn()

    def end_game(self, winner=None):
            """Finish the game and determine the winner."""
            # Record the winner or draw.
            self.playing = False
            self.game_over = True
            self.winner = winner
            self.turn_started_at = None

    def handle_move(self, letter):

        letter = letter.upper()
        
        if(letter == "Z"):
            self.ui.game_gui.flash_text(
                "FORFEIT",
                self.ui.game_gui.invalid_move_flash_colour
            ) 
            self.end_game(1 - self.current_player)
            return

        # Check whether the cell exists
        if letter < "A" or letter > "Y":
            print("Invalid move: Cell does not exist")
            self.end_game(1 - self.current_player)
            return

        # Convert letter to board coordinates
        index = ord(letter) - ord("A")

        row = index // 5
        col = index % 5

        # Check whether the cell is active
        if self.board.grid[row][col] == 0:
            print("Invalid move: Cell is empty")
            self.ui.game_gui.flash_text(
                "INVALID MOVE",
                self.ui.game_gui.invalid_move_flash_colour
            ) 
            self.end_game(1 - self.current_player)
            return

        print(f"Valid move: {letter} at row {row}, column {col}")

        # Execute the move here
        new_state, points, was_hinger = self.board.simulate_move(self.board, letter)
        if was_hinger:
            self.ui.game_gui.flash_text(
                "HINGER!",
                self.ui.game_gui.hinger_flash_colour
            )      
        # Update board and score
        self.board = new_state
        self.scores[self.current_player] += points
        
        # Animate gain wiht GUI
        
        # Determine the current player's name
        player_name = None
        if self.current_player == 0:
            player_name = "Human" if self.agentA is None else "Computer A"
        else:
            player_name = "Human" if self.agentB is None else (
                "Computer" if self.versus else "Computer B"
            )
        # Record player name and move
        self.move_history.append((player_name, letter, was_hinger))
        print(f"Player {player_name} played {letter}")
        print(f"Points earned: {points}")

        # Check whether all counters have been removed
        if all(cell == 0 for row in self.board.grid for cell in row):

            if self.scores[0] > self.scores[1]:
                winner = 0
            elif self.scores[1] > self.scores[0]:
                winner = 1
            else:
                winner = None

            self.finish_turn()
            self.end_game(winner)
            return

        # End current player's turn and start opponent's turn
        self.next_turn()
        
    def next_turn(self):
            """Switch between Player A and Player B."""
            # Record the current player's time
            self.finish_turn()
            
            # Check if any hingers remain, if not end game?!
            #if(self.board.numHingers(self) < 1):
                #return
                
            # Switch player
            self.current_player = 1 - self.current_player
            # Start the new player's timer
            self.start_turn()

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