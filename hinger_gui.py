"""The gam UI for our Hinger game."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame
from a1_state import State

# GUI Colours
BACKGROUND = (17, 24, 39)
PANEL      = (31, 41, 55)
ACTIVE     = (22, 107, 82)
EMPTY      = (55, 65, 81)
SELECTED   = (37, 99, 235)
TEXT       = (249, 250, 251)

class HingerGUI:

    def __init__(self, state):
        """Initialise the Hinger graphical interface."""

        pygame.init()

        self.state = state

        # Window dimensions
        self.width = 800
        self.height = 700

        # Create the window
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Hinger")

        # Fonts
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 42, bold=True)

        # Board layout
        self.cell_size = 80
        self.cell_gap = 8

        self.board_x = 180
        self.board_y = 160

        # Currently selected cell
        self.selected = None

        # Main loop control
        self.running = True

        self.clock = pygame.time.Clock()
        
    def draw_board(self):
        """Draw the 5x5 Hinger board."""

        for row in range(5):
            for col in range(5):

                # Calculate cell position
                x = self.board_x + col * (
                    self.cell_size + self.cell_gap
                    )

                y = self.board_y + row * (
                    self.cell_size + self.cell_gap
                    )

                # Determine whether cell contains a counter
                active = self.state.grid[row][col] == 1

                colour = ACTIVE if active else EMPTY

                # Calculate cell letter
                letter = chr(ord("A") + row * 5 + col)

                if self.selected == letter:
                    colour = SELECTED

                rect = pygame.Rect(
                    x, y,
                    self.cell_size,
                    self.cell_size
                    )

                pygame.draw.rect(
                    self.screen,
                    colour,
                    rect,
                    border_radius=8
                    )

                # Draw the letter in the centre
                text = self.font.render(letter, True, TEXT)

                text_rect = text.get_rect(center=rect.center)

                self.screen.blit(text, text_rect)

    def run(self):
        """Run the graphical interface."""

        while self.running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

            # Clear screen
            self.screen.fill(BACKGROUND)

            # Draw title
            title = self.title_font.render(
                "HINGER",
                True,
                TEXT
            )

            self.screen.blit(title, (320, 50))

            # Draw board
            self.draw_board()

            # Update display
            pygame.display.flip()

            # Limit to 60 FPS
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":

    grid = [[1 for col in range(5)] for row in range(5)]

    state = State(grid)

    gui = HingerGUI(state)

    gui.run()