"""Defines the number of players scene GUI in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame
from UI import Button
from scene_manager import Scene


class NumPlayersSceneGUI:

    def __init__(self, gui):
        self.gui = gui

        self.vs_ai_button = Button(
            0, 0, 240, 60,
            "VS AI",
            callback=self.vs_ai
        )

        self.spectate_button = Button(
            0, 0, 240, 60,
            "SPECTATE",
            callback=self.spectate
        )

        self.back_button = Button(
            0, 0, 140, 50,
            "BACK",
            callback=self.go_back
        )

        self.buttons = [
            self.vs_ai_button,
            self.spectate_button,
            self.back_button
        ]

    def draw(self):
        """Draw the player selection screen."""

        screen = self.gui.screen
        width = self.gui.width
        height = self.gui.height

        # Question
        font = pygame.font.SysFont(
            "Segoe UI", 28, bold=True
        )

        question = font.render(
            "HOW MANY PLAYERS?",
            True,
            (255, 255, 255)
        )

        screen.blit(
            question,
            question.get_rect(
                center=(width // 2, int(height * 0.32))
            )
        )

        # Centre buttons
        self.vs_ai_button.rect.center = (
            width // 2,
            int(height * 0.48)
        )

        self.spectate_button.rect.center = (
            width // 2,
            int(height * 0.60)
        )

        self.back_button.rect.center = (
            width // 2,
            int(height * 0.78)
        )

        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        """Handle button interactions."""

        for button in self.buttons:
            button.handle_event(event)

    def vs_ai(self):
        """Choose human vs AI."""
        self.gui.game.set_players(True)
        self.gui.scene.change_scene(Scene.STRATEGY)

    def spectate(self):
        """Choose AI vs AI."""
        self.gui.game.set_players()
        self.gui.scene.change_scene(Scene.STRATEGY)

    def go_back(self):
        """Return to home."""
        self.gui.scene.change_scene(Scene.HOME)
