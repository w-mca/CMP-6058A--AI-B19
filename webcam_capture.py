# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import pickle
import cv2
import mediapipe as mp
import numpy as np
import pygame

# Load the trained model once when this module is imported so the game stays fast
with open("best_asl_model.pkl", "rb") as f:
    MODEL = pickle.load(f)


class WebcamCapture:

    def __init__(self, gui):
        self.gui = gui
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.FINGERTIP_IDS = [4, 8, 12, 16, 20]

        self.cap = None
        self.hands = None
        self.camera_active = False

        self.WINDOW_NAME = "ASL Game Input - Press SPACE to Confirm"


    def camera_on(self):
        """Turn on the webcam and initialise hand tracking."""

        if self.camera_active:
            return

        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            self.cap.release()
            self.cap = None
            raise RuntimeError("Could not open webcam.")

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

        self.camera_active = True


    def camera_off(self):
        """Turn off the webcam and release resources."""

        if not self.camera_active:
            return

        if self.hands is not None:
            self.hands.close()
            self.hands = None

        if self.cap is not None:
            self.cap.release()
            self.cap = None

        cv2.destroyAllWindows()

        self.camera_active = False


    def _extract_68_features(self, hand_landmarks) -> list:
        """Applies exact Task 6 preprocessing (wrist shift, max-dist scale, 5 tip distances)."""

        coords = np.array(
            [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark],
            dtype=float
        )

        # Position invariance (shift origin to wrist)
        wrist = coords[0].copy()
        coords = coords - wrist

        # Scale invariance
        max_dist = np.max(np.linalg.norm(coords, axis=1))

        if max_dist > 0:
            coords = coords / max_dist

        # Engineered features
        tip_distances = [
            np.linalg.norm(coords[tip_id])
            for tip_id in self.FINGERTIP_IDS
        ]

        return list(coords.flatten()) + tip_distances


    def capture_sign_letter(self) -> str | None:
        """Process a single webcam frame and return a confirmed letter."""

        if not self.camera_active:
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.flip(frame, 1)

        H, W, _ = frame.shape

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        current_prediction = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Draw hand landmarks
            self.mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style(),
            )

            # Predict letter for the current frame
            features = self._extract_68_features(hand_landmarks)
            raw_pred = MODEL.predict([features])[0]
            current_prediction = str(raw_pred).strip().upper()

            # Draw bounding box
            x_vals = [lm.x for lm in hand_landmarks.landmark]
            y_vals = [lm.y for lm in hand_landmarks.landmark]

            x1 = max(0, int(min(x_vals) * W) - 15)
            y1 = max(0, int(min(y_vals) * H) - 15)
            x2 = min(W, int(max(x_vals) * W) + 15)
            y2 = min(H, int(max(y_vals) * H) + 15)

            cv2.rectangle(
                frame, (x1, y1), (x2, y2), (0, 255, 0), 2
            )

            cv2.putText(
                frame,
                f"Detected: {current_prediction}",
                (x1, max(35, y1 - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.1,
                (0, 255, 0),
                3,
                cv2.LINE_AA,
            )

        # On-screen prompt
        prompt = (
            f"Press SPACE to lock in '{current_prediction}'"
            if current_prediction
            else "Show hand to sign... (Q to quit)"
        )

        cv2.putText(
            frame,
            prompt,
            (15, H - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        # Display the camera feed inside the game window
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        surface = pygame.image.frombuffer(
            frame.tobytes(),
            (W, H),
            "RGB"
        )
        
        # Calculate the available space beside the board
        width = self.gui.width
        height = self.gui.height
        margin = 20
        
        board_size = int(min(width, height) * 0.58)
        board_right = (width + board_size) // 2
        
        available_width = width - board_right - margin * 2
        available_height = height - margin * 2
        
        if available_width > 0 and available_height > 0:
        
            # Scale the camera to fill the available space
            scale = min(
                available_width / W,
                available_height / H
            )
        
            camera_width = int(W * scale)
            camera_height = int(H * scale)
        
            surface = pygame.transform.smoothscale(
                surface,
                (camera_width, camera_height)
            )
        
            # Centre the camera beside the board
            x = board_right + margin
            x += (available_width - camera_width) // 2
            y = (height - camera_height) // 2
        
            self.gui.screen.blit(surface, (x, y))
        
        # Confirm the predicted letter
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if current_prediction is not None:
                return current_prediction
        
        return None


# Quick standalone test if you run this file directly
if __name__ == "__main__":

    webcam = WebcamCapture()
    webcam.camera_on()

    letter = None

    try:
        while webcam.camera_active and letter is None:
            letter = webcam.capture_sign_letter()
    finally:
        webcam.camera_off()

    print(f"Returned to game: {letter!r} (type: {type(letter).__name__})")