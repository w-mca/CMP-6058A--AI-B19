"""Defines the strategy scene gui in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame
from UI import Button, Selector
from scene_manager import Scene

class StrategySceneGUI:

    STRATEGIES = ["Minimax", "Alpha-Beta", "MCTS"]

    def __init__(self, gui):
        self.gui = gui

        self.agent_a_selector = Selector(
            0, 0, 200, 50,
            self.STRATEGIES,
            callback=self.set_agent_a_strategy
        )

        self.agent_b_selector = Selector(
            0, 0, 200, 50,
            self.STRATEGIES,
            callback=self.set_agent_b_strategy
        )

        self.back_button = Button(
            0, 0, 140, 50,
            "BACK",
            callback=self.go_back
        )

        self.continue_button = Button(
            0, 0, 180, 50,
            "CONTINUE",
            callback=self.continue_game
        )

        self.agent_a_strategy = None
        self.agent_b_strategy = None

    def draw_text(self, text, x, y, size=24):
        """Draw centred text."""

        font = pygame.font.SysFont(
            "Segoe UI", size, bold=True
        )

        surface = font.render(
            text, True, (255, 255, 255)
        )

        self.gui.screen.blit(
            surface,
            surface.get_rect(center=(x, y))
        )

    def draw(self):
        """Draw strategy selection based on game mode."""

        width = self.gui.width
        height = self.gui.height
        versus = self.gui.game.versus

        self.draw_text(
            "SELECT YOUR STRATEGY",
            width // 2,
            int(height * 0.25),
            28
        )

        if versus:
            # Human vs AI: only Agent B needs a strategy.
            self.draw_text(
                "AGENT B",
                width // 2,
                int(height * 0.35)
            )

            self.agent_b_selector.set_position(
                (width - 200) // 2,
                int(height * 0.40)
            )

            self.agent_b_selector.draw(self.gui.screen)

        else:
            # Agent vs Agent: configure both independently.
            left_x = width // 4
            right_x = width * 3 // 4

            self.draw_text(
                "AGENT A", left_x, int(height * 0.35)
            )
            self.draw_text(
                "AGENT B", right_x, int(height * 0.35)
            )

            self.agent_a_selector.set_position(
                left_x - 100,
                int(height * 0.40)
            )

            self.agent_b_selector.set_position(
                right_x - 100,
                int(height * 0.40)
            )

            self.agent_a_selector.draw(self.gui.screen)
            self.agent_b_selector.draw(self.gui.screen)

        self.back_button.rect.center = (
            width // 2 - 100,
            int(height * 0.85)
        )

        self.continue_button.rect.center = (
            width // 2 + 100,
            int(height * 0.85)
        )

        self.back_button.draw(self.gui.screen)
        self.continue_button.draw(self.gui.screen)

    def handle_event(self, event):
        """Handle clicks on active selectors and buttons."""

        if self.gui.game.versus:
            self.agent_b_selector.handle_event(event)
        else:
            self.agent_a_selector.handle_event(event)
            self.agent_b_selector.handle_event(event)

        self.back_button.handle_event(event)
        self.continue_button.handle_event(event)

    def set_agent_a_strategy(self, strategy):
        self.agent_a_strategy = strategy.lower().replace("-", "")

    def set_agent_b_strategy(self, strategy):
        self.agent_b_strategy = strategy.lower().replace("-", "")

    def go_back(self):
        self.gui.scene.change_scene(Scene.NUMPLAYERS)

    def continue_game(self):
        """Proceed only after required strategies are chosen."""

        if self.agent_b_strategy is None:
            return

        if not self.gui.game.versus:
            if self.agent_a_strategy is None:
                return

        # Store strategies in the game controller.
        self.gui.game.strategyA = self.agent_a_strategy
        self.gui.game.strategyB = self.agent_b_strategy

        self.gui.scene.change_scene(Scene.GAME)