# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import pickle
import cv2
import mediapipe as mp
import numpy as np

# 1. Load the winning model saved by training_and_optimisation.py (Task 7)
with open("best_asl_model.pkl", "rb") as f:
    model = pickle.load(f)

# 2. Set up MediaPipe Hands for live video stream (static_image_mode=False)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# 3. Open default webcam (0)
cap = cv2.VideoCapture(0)
fingertip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips

print("Webcam started! Hold your right hand up to sign. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from webcam.")
        break

    # Flip horizontally for a natural mirror view
    frame = cv2.flip(frame, 1)
    H, W, _ = frame.shape

    # Convert BGR (OpenCV) to RGB (MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Draw the 21 hand landmarks & skeleton lines on screen
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style(),
        )

        # Extract raw (21, 3) coordinates and screen coordinates for the bounding box
        raw_coords = []
        x_screen = []
        y_screen = []

        for lm in hand_landmarks.landmark:
            raw_coords.append([lm.x, lm.y, lm.z])
            x_screen.append(lm.x)
            y_screen.append(lm.y)

        coords = np.array(raw_coords, dtype=float)

        # --- EXACT SAME TASK 6 PREPROCESSING (68 FEATURES) ---
        # Position invariance: shift origin to wrist (Landmark 0)
        wrist = coords[0].copy()
        coords = coords - wrist

        # Scale invariance: divide by maximum Euclidean distance from wrist
        max_dist = np.max(np.linalg.norm(coords, axis=1))
        if max_dist > 0:
            coords = coords / max_dist

        # Feature engineering: 5 wrist-to-fingertip Euclidean distances
        tip_distances = [np.linalg.norm(coords[tip_id]) for tip_id in fingertip_ids]

        # Combine 63 normalised coordinates + 5 fingertip distances = 68 features
        feature_vector = list(coords.flatten()) + tip_distances

        # Predict ASL letter using your trained model
        prediction = model.predict([feature_vector])[0]

        # Draw bounding box and predicted letter above the hand
        x1 = max(0, int(min(x_screen) * W) - 15)
        y1 = max(0, int(min(y_screen) * H) - 15)
        x2 = min(W, int(max(x_screen) * W) + 15)
        y2 = min(H, int(max(y_screen) * H) + 15)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Sign: {str(prediction).upper()}",
            (x1, max(30, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (0, 255, 0),
            3,
            cv2.LINE_AA,
        )

    cv2.imshow("ASL Real-Time Translator (Group B19)", frame)

    # Press 'q' to exit cleanly
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

