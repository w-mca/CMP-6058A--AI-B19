"""Defines the game scene GUI in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame


class GameSceneGUI:

    BACKGROUND = (17, 24, 39)
    PANEL = (31, 41, 55)
    ACTIVE = (22, 107, 82)
    EMPTY = (55, 65, 81)
    TEXT = (249, 250, 251)
    SELECTED = (37, 99, 235)

    def __init__(self, gui):
        self.gui = gui
        self.cell_rects = {}

    def draw(self):
        game = self.gui.game
        screen = self.gui.screen

        if game.board is None:
            return

        width = self.gui.width
        height = self.gui.height
        size = min(width, height)

        title_font = pygame.font.SysFont(
            "Arial", max(18, int(size * 0.045)), bold=True
        )
        info_font = pygame.font.SysFont(
            "Arial", max(14, int(size * 0.025))
        )

        # Current player
        player_name = "Player A" if game.current_player == 0 else "Player B"

        title = title_font.render(
            f"{player_name}'s Turn", True, self.TEXT
        )
        screen.blit(title, title.get_rect(center=(width // 2, int(height * 0.08))))

        # Scores
        score_text = info_font.render(
            f"Player A: {game.scores[0]}     Player B: {game.scores[1]}",
            True,
            self.TEXT
        )
        screen.blit(
            score_text,
            score_text.get_rect(center=(width // 2, int(height * 0.15)))
        )

        # Countdown
        remaining = game.get_remaining_time()

        timer_text = info_font.render(
            f"Time remaining: {remaining:.1f}s",
            True,
            self.TEXT
        )
        screen.blit(
            timer_text,
            timer_text.get_rect(center=(width // 2, int(height * 0.21)))
        )

        # Total time, including the current turn
        totals = game.total_time_used.copy()

        if game.playing:
            totals[game.current_player] += game.get_turn_time_used()

        total_text = info_font.render(
            f"Total time: A {totals[0]:.1f}s | B {totals[1]:.1f}s",
            True,
            self.TEXT
        )
        screen.blit(
            total_text,
            total_text.get_rect(center=(width // 2, int(height * 0.27)))
        )

        # Board layout
        board_size = int(size * 0.58)
        gap = max(3, int(size * 0.012))
        cell_size = (board_size - 4 * gap) // 5

        actual_size = 5 * cell_size + 4 * gap
        board_x = (width - actual_size) // 2
        board_y = int(height * 0.34)

        self.cell_rects.clear()

        for row in range(5):
            for col in range(5):
                x = board_x + col * (cell_size + gap)
                y = board_y + row * (cell_size + gap)

                rect = pygame.Rect(x, y, cell_size, cell_size)

                # Active cells are represented by 1
                active = game.board.grid[row][col] == 1
                colour = self.ACTIVE if active else self.EMPTY

                pygame.draw.rect(
                    screen, colour, rect, border_radius=8
                )

                letter = chr(ord("A") + row * 5 + col)

                label = info_font.render(letter, True, self.TEXT)
                screen.blit(label, label.get_rect(center=rect.center))

                self.cell_rects[letter] = rect

        if game.game_over:
            winner_text = (
                "Draw!" if game.winner is None
                else f"Winner: {game.winner}"
            )

            message = title_font.render(winner_text, True, self.TEXT)
            screen.blit(
                message,
                message.get_rect(center=(width // 2, int(height * 0.93)))
            )

    def handle_event(self, event):
        """Handle keyboard input during a human player's turn."""

        game = self.gui.game

        if not game.playing or game.game_over:
            return

        # Check whether the current player is human
        agent = game.agentA if game.current_player == 0 else game.agentB

        if agent is not None:
            return

        if event.type == pygame.KEYDOWN:

            # Only accept A-Z
            if pygame.K_a <= event.key <= pygame.K_z:

                letter = chr(ord("A") + event.key - pygame.K_a)

                game.handle_move(letter)