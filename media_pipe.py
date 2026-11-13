import mediapipe as mp
import cv2

print("MediaPipe version:", mp.__version__)
print("OpenCV version:", cv2.__version__)

import mediapipe as mp

print(mp.tasks.vision.HandLandmarker)


import cv2
import mediapipe as mp
from pathlib import Path

# Folder containing your image and model
folder = Path(r"C:\Users\adamb\OneDrive\Documents\AI coursework")

# Change this to your actual image filename
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

image_path = filedialog.askopenfilename(
    title="Select your ASL image",
    filetypes=[("Images", "*.jpg *.jpeg *.png")]
)

root.destroy()

if not image_path:
    raise ValueError("No image selected")

model_path = folder / "hand_landmarker.task"

# Load the image
image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Image not found: {image_path}")

height, width = image.shape[:2]

# Set up MediaPipe
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
Options = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = Options(
    base_options=BaseOptions(
        model_asset_path=str(model_path)
    ),
    running_mode=RunningMode.IMAGE,
    num_hands=2
)

# Detect the hands
with HandLandmarker.create_from_options(options) as detector:
    mp_image = mp.Image.create_from_file(str(image_path))
    result = detector.detect(mp_image)

# Connections between the 21 landmarks
connections = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]

# Draw the landmarks
for hand in result.hand_landmarks:
    points = []

    for i, landmark in enumerate(hand):
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        points.append((x, y))

        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)

        cv2.putText(
            image, str(i), (x + 5, y - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 0, 255), 1
        )

    for start, end in connections:
        cv2.line(
            image, points[start], points[end],
            (255, 0, 0), 2
        )

