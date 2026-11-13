# recognition for the asl sign language photos of hand
# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William


import cv2
import mediapipe as mp
from tkinter import Tk, filedialog

from pathlib import Path


folder = Path(r"C:\Users\adamb\OneDrive\Documents\AI coursework")

images = [
    file for file in folder.iterdir()
    if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
]

print("Images found:", images)

# Check that images exist
if not images:
    raise FileNotFoundError("No images found in the folder")

image_path = str(images[0])

print("Using image:", image_path)

image = cv2.imread(image_path)

if image is None:
    raise ValueError("Image could not be loaded")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
) as hands:

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_image)

vector = []

if results.multi_hand_landmarks:

    for landmark in results.multi_hand_landmarks[0].landmark:
        vector.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    mp_draw.draw_landmarks(
        image,
        results.multi_hand_landmarks[0],
        mp_hands.HAND_CONNECTIONS
    )

else:
    vector = [0.0] * 63
    print("No hand detected")

print("Landmark vector:", vector)
print("Number of values:", len(vector))

import matplotlib.pyplot as plt

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 8))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("ASL Hand Landmarks")
plt.show()

import matplotlib.pyplot as plt

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10, 8))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("ASL Hand Landmarks")
plt.show()

import numpy as np

landmark_vector = np.array(vector, dtype=float)

np.savetxt(
    folder / "asl_coordinates.csv",
    landmark_vector.reshape(1, 63),
    delimiter=","
)

cv2.imwrite(
    str(folder / "asl_landmarks.jpg"),
    image
)

print("Coordinates and image saved successfully!")
