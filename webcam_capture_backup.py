# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import pickle
import cv2
import mediapipe as mp
import numpy as np

# Load the trained model once when this module is imported so the game stays fast
with open("best_asl_model.pkl", "rb") as f:
    MODEL = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

FINGERTIP_IDS = [4, 8, 12, 16, 20]


def _extract_68_features(hand_landmarks) -> list:
    """Applies exact Task 6 preprocessing (wrist shift, max-dist scale, 5 tip distances)."""
    coords = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark], dtype=float)

    # 1. Position invariance (shift origin to wrist)
    wrist = coords[0].copy()
    coords = coords - wrist

    # 2. Scale invariance (normalise by max Euclidean distance from wrist)
    max_dist = np.max(np.linalg.norm(coords, axis=1))
    if max_dist > 0:
        coords = coords / max_dist

    # 3. Engineered features (5 wrist-to-fingertip distances)
    tip_distances = [np.linalg.norm(coords[tip_id]) for tip_id in FINGERTIP_IDS]

    return list(coords.flatten()) + tip_distances


def capture_sign_letter(camera_index: int = 0) -> str | None:
    """
    Opens the webcam, shows live ASL predictions, and returns the predicted
    letter as an uppercase string (e.g. 'A') when the user presses SPACEBAR.
    Returns None if the user presses 'q' or ESC to cancel.
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    captured_letter = None
    current_prediction = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        current_prediction = None

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            # Predict letter for the current frame
            features = _extract_68_features(hand_landmarks)
            raw_pred = MODEL.predict([features])[0]
            current_prediction = str(raw_pred).strip().upper()

            # Draw bounding box + live preview label
            x_vals = [lm.x for lm in hand_landmarks.landmark]
            y_vals = [lm.y for lm in hand_landmarks.landmark]
            x1 = max(0, int(min(x_vals) * W) - 15)
            y1 = max(0, int(min(y_vals) * H) - 15)
            x2 = min(W, int(max(x_vals) * W) + 15)
            y2 = min(H, int(max(y_vals) * H) + 15)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
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

        # On-screen prompt so the player knows how to lock in their guess
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

        cv2.imshow("ASL Game Input - Press SPACE to Confirm", frame)
        key = cv2.waitKey(1) & 0xFF

        # ASCII 32 is the SPACEBAR
        if key == 32:
            if current_prediction is not None:
                captured_letter = current_prediction
                break
            else:
                print("No hand detected—hold your sign up before pressing Spacebar!")

        # 'q' or ESC (27) cancels without locking in a letter
        elif key in (ord("q"), 27):
            break

    hands.close()
    cap.release()
    cv2.destroyAllWindows()

    return captured_letter


# Quick standalone test if you run this file directly
if __name__ == "__main__":
    letter = capture_sign_letter()
    print(f"Returned to game: {letter!r} (type: {type(letter).__name__})")