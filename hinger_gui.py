
"""The game UI for our Hinger game."""

# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)
import pygame
from a1_state import State
from scene_manager import Scene, SceneManager
from home_scene_gui import HomeSceneGUI
from numplayers_scene_gui import NumPlayersSceneGUI
from strategy_scene_gui import StrategySceneGUI

# GUI Colours
BACKGROUND = (17, 24, 39)
PANEL = (31, 41, 55)
ACTIVE = (22, 107, 82)
EMPTY = (55, 65, 81)
SELECTED = (37, 99, 235)
TEXT = (249, 250, 251)


class HingerGUI:

    def __init__(self, game):
        """Initialise the Hinger graphical interface."""
        self.game = game
        pygame.init()
        self.scene = SceneManager()
        self.home_gui = HomeSceneGUI(self)
        self.numplayers_gui = NumPlayersSceneGUI(self)
        self.strategy_gui = StrategySceneGUI(self)
       # self.state = state

        # Initial window dimensions
        self.width = 700
        self.height = 700

        # Create a resizable window
        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.RESIZABLE
        )

        # Currently selected cell
        self.selected = None

        # Main loop control
        self.running = True
        self.clock = pygame.time.Clock()

        # Calculate the initial layout
        self.update_layout()
    

    def update_layout(self):
        """Scale and centre the title and board together."""

        # Use the smaller window dimension for scaling
        size = min(self.width, self.height)

        # Scale title font
        self.title_font = pygame.font.SysFont(
            "Arial",
            max(18, int(size * 0.055)),
            bold=True
        )

        title_height = self.title_font.get_height()

        # Gap between title and board
        title_gap = int(size * 0.06)

        # Board occupies 65% of the smaller dimension
        board_size = int(size * 0.65)

        # Scale the gaps between cells
        self.cell_gap = max(2, int(size * 0.012))

        # Calculate individual cell size
        self.cell_size = max(
            1,
            (board_size - 4 * self.cell_gap) // 5
        )

        # Actual total board size
        total_board_size = (
            5 * self.cell_size + 4 * self.cell_gap
        )

        # Calculate total height of title + gap + board
        group_height = (
            title_height + title_gap + total_board_size
        )

        # Centre the entire group vertically
        group_top = (self.height - group_height) // 2

        # Centre board horizontally
        self.board_x = (
            self.width - total_board_size
        ) // 2

        # Position board below title
        self.board_y = (
            group_top + title_height + title_gap
        )

        # Title position
        self.title_y = group_top

        # Scale cell lettering
        self.font = pygame.font.SysFont(
            "Arial",
            max(12, int(self.cell_size * 0.35))
        )
        
    def run(self):
        """Run the main GUI loop."""

        while self.running:

            # Handle events
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.size
                    self.update_layout()

                # Send events to the active scene
                match self.scene.current_scene:

                    case Scene.HOME:
                        self.home_gui.handle_event(event)

                    case Scene.NUMPLAYERS:
                        self.numplayers_gui.handle_event(event)

                    case Scene.STRATEGY:
                        self.strategy_gui.handle_event(event)

            # Clear screen
            self.screen.fill(BACKGROUND)

            # Draw current scene
            match self.scene.current_scene:

                case Scene.HOME:
                    self.home_gui.draw()

                case Scene.NUMPLAYERS:
                    self.numplayers_gui.draw()

                case Scene.STRATEGY:
                    self.strategy_gui.draw()

                case Scene.GAME:
                    pass

                case Scene.SETTINGS:
                    pass

            # Update display
            pygame.display.flip()

            # Limit to 60 FPS
            self.clock.tick(60)

        pygame.quit()

def tester():
    """Test the Hinger graphical interface."""

    # Create a full 5x5 board
    grid = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]

    state = State(grid)

    gui = HingerGUI(None)

    gui.run()


if __name__ == "__main__":
    tester()
