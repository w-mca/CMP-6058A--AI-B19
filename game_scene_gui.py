"""Defines the game scene GUI in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame
from scene_manager import Scene


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
        
        # Text flash anim
        self.hinger_flash_colour = (255, 215, 0)
        self.invalid_move_flash_colour = (239, 68, 68)
        
        self.flash_message = None
        self.flash_color = (255, 255, 255)
        self.flash_start = 0
        self.flash_duration = 1500

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
        
        # Get current player's agent and strategy
        if game.current_player == 0:
            agent = game.agentA
            strategy = game.agentA.strategy
        else:
            agent = game.agentB
            strategy = game.agentB.strategy

        # Draw strategy badge for AI players only
        if agent is not None and strategy is not None:

            strategy_names = {
                "minimax": "MINIMAX",
                "alphabeta": "ALPHA-BETA",
                "mcts": "MCTS"
                }

            strategy_text = strategy_names.get(strategy, strategy.upper())

            badge_font = pygame.font.SysFont(
                "Arial", max(12, int(size * 0.020)), bold=True
            )

            label = badge_font.render(strategy_text, True, self.TEXT)

            # Badge dimensions
            padding_x = 14
            padding_y = 7

            badge_width = label.get_width() + padding_x * 2
            badge_height = label.get_height() + padding_y * 2

            # Position underneath player name
            badge = pygame.Rect(
                0, 0, badge_width, badge_height
            )
            badge.center = (width // 2, int(height * 0.12))

            # Green rounded background
            pygame.draw.rect(
                screen, self.ACTIVE, badge, border_radius=8
            )

            # White strategy text
            screen.blit(label, label.get_rect(center=badge.center))

        # Say whos turn it is
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
        if game.game_over == False:
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
                
        #display winner, button to play again
        if game.game_over:

            if game.winner is None:
                winner_text = "Draw!"

            elif game.versus:
                # Human vs Computer
                winner_text = (
                "Winner: Human"
                if game.winner == 0
                    else "Winner: Computer"
                )
            else:
                # Computer A vs Computer B
                winner_text = (
                    "Winner: Computer A"
                    if game.winner == 0
                        else "Winner: Computer B"
                        )
            message = title_font.render(winner_text, True, self.TEXT)
            screen.blit(
                message,
                message.get_rect(center=(width // 2, int(height * 0.5)))
            )
            # Play Again button
            button_width = int(size * 0.25)
            button_height = int(size * 0.07)

            self.play_again_rect = pygame.Rect(
                0, 0, button_width, button_height
            )

            self.play_again_rect.center = (
                width // 2,
                int(height * 0.60)
            )

            # Green rounded rectangle
            pygame.draw.rect(
                screen,
                self.ACTIVE,
                self.play_again_rect,
                border_radius=10
            )

            # White button text
            button_text = info_font.render(
                "Play Again", True, self.TEXT
            )

            screen.blit(
                button_text,
                button_text.get_rect(center=self.play_again_rect.center)
            )
            
        if self.flash_message is not None:
            elapsed = pygame.time.get_ticks() - self.flash_start

            if elapsed >= self.flash_duration:
                self.flash_message = None

            else:
                progress = elapsed / self.flash_duration

                # Fade from fully visible to transparent
                alpha = int(255 * (1 - progress))

                flash_font = pygame.font.SysFont(
                    "Arial", max(36, int(size * 0.09)), bold=True
                )

                flash_surface = flash_font.render(
                    self.flash_message, True, self.flash_color
                )

                flash_surface.set_alpha(alpha)

                flash_rect = flash_surface.get_rect(
                    center=(width // 2, height // 2)
                )

                screen.blit(flash_surface, flash_rect)
            
    def flash_text(self, message, color=(255, 255, 255), duration=1500):
        """Display temporary text in the centre of the screen."""
        self.flash_message = message
        self.flash_color = color
        self.flash_duration = duration
        self.flash_start = pygame.time.get_ticks()
        
    def handle_event(self, event):
        """Handle keyboard input during a human player's turn."""

        game = self.gui.game

###################
        # Handle Play Again button
        if game.game_over:

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (hasattr(self, "play_again_rect")
                            and self.play_again_rect.collidepoint(event.pos)
                            ):
                        self.gui.scene.change_scene(Scene.HOME)

            return

        if not game.playing:
            return

################

        # Check whether the current player is human
        agent = game.agentA if game.current_player == 0 else game.agentB

        if agent is not None:
            if(agent.moving):
                return
            agent.moving = True             
            game.handle_move(agent.next_move(game.board)[0])
            return

        if event.type == pygame.KEYDOWN:

            # Only accept A-Z
            if pygame.K_a <= event.key <= pygame.K_z:

                letter = chr(ord("A") + event.key - pygame.K_a)

                game.handle_move(letter)