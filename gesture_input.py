"""The main logic for Gesture input"""
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William.

import cv2
import mediapipe as mp


class GestureInput:

    def __init__(self):
        """Initialise MediaPipe hand tracking."""

        base_options = mp.tasks.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_hands=2
        )

        self.detector = mp.tasks.vision.HandLandmarker.create_from_options(
            options
        )

        # Connections between the 21 hand landmarks
        self.connections = mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS

    def process(self, frame):
        """Detect hands and draw their landmarks onto the image."""

        # Convert OpenCV BGR image to RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.detector.detect(image)

        height, width = frame.shape[:2]

        for hand in result.hand_landmarks:

            # Draw connections between landmarks
            for connection in self.connections:
                start = hand[connection.start]
                end = hand[connection.end]

                start_point = (
                    int(start.x * width),
                    int(start.y * height)
                )

                end_point = (
                    int(end.x * width),
                    int(end.y * height)
                )

                cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

            # Draw all 21 landmark points
            for landmark in hand:
                point = (
                    int(landmark.x * width),
                    int(landmark.y * height)
                )

                cv2.circle(frame, point, 4, (0, 0, 255), -1)

        return frame

    def close(self):
        """Release MediaPipe resources."""
        self.detector.close()