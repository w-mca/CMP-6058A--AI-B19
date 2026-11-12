"""Defines the home scene gui in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import pygame
from UI import Button
from scene_manager import Scene

class HomeSceneGUI:

    def __init__(self, gui):
        self.gui = gui

        self.play_button = Button(
            x=0,
            y=0,
            width=200,
            height=60,
            text="PLAY",
            callback=self.start_game
        )

    def draw(self):
        """Draw the home scene."""

        title = self.gui.title_font.render(
            "HINGER",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(self.gui.width // 2, 150)
        )

        self.gui.screen.blit(title, title_rect)

        # Keep button centred when resizing
        self.play_button.set_position(
            (self.gui.width - 200) // 2,
            self.gui.height // 2
        )

        self.play_button.draw(self.gui.screen)

    def handle_event(self, event):
        self.play_button.handle_event(event)

    def start_game(self):
        self.gui.scene.change_scene(Scene.NUMPLAYERS)
        print("Changing scene to nunplayers")