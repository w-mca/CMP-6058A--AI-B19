"""Manage the different scenes in Hinger."""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
from enum import Enum, auto


class Scene(Enum):
    HOME = auto()
    NUMPLAYERS = auto()
    STRATEGY = auto()
    GAME = auto()
    SETTINGS = auto()


class SceneManager:

    def __init__(self):
        """Initialise the scene manager."""
        self.current_scene = Scene.HOME

    def change_scene(self, scene: Scene):
        """Switch to another scene."""
        self.current_scene = scene

    def is_scene(self, scene: Scene) -> bool:
        """Check whether a scene is currently active."""
        return self.current_scene == scene
    
    def get_scene(self, scene: Scene) -> Scene:
        """Return the scene that is currently active."""
        return self.current_scene