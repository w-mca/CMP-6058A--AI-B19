
"""The game UI for our Adv Hinger game camera feed"""

# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William
import cv2
import pygame


class CameraFeedGUI:

    def __init__(self, gui):
        """Initialise the live camera feed."""
        self.gui = gui
        self.camera = None

    def start(self):
        """Open the webcam."""
        if self.camera is None:
            self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

            if not self.camera.isOpened():
                self.camera.release()
                self.camera = None

    def stop(self):
        """Release the webcam."""
        if self.camera is not None:
            self.camera.release()
            self.camera = None

    def draw(self):
        """Draw a square live camera feed."""
        if self.camera is None:
            self.start()

        if self.camera is None:
            return

        success, frame = self.camera.read()

        if not success:
            return

        # Convert OpenCV BGR image to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Crop the image into a square
        height, width = frame.shape[:2]
        side = min(width, height)

        x = (width - side) // 2
        y = (height - side) // 2

        frame = frame[y:y + side, x:x + side]

        # Mirror the camera image
        frame = cv2.flip(frame, 1)

        # Convert the image to a Pygame surface
        surface = pygame.image.frombuffer(
            frame.tobytes(),
            (side, side),
            "RGB"
        )

        # Scale the feed relative to the window
        size = max(80, int(min(self.gui.width, self.gui.height) * 0.20))
        surface = pygame.transform.smoothscale(surface, (size, size))

        # Position the camera in the top-right corner
        rect = surface.get_rect(
            topright=(self.gui.width - 15, 15)
        )

        self.gui.screen.blit(surface, rect)

        # Draw a border around the feed
        pygame.draw.rect(
            self.gui.screen,
            (249, 250, 251),
            rect,
            2,
            border_radius=4
        )