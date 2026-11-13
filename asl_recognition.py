# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:55:25 2026

@author: adamb
"""


import cv2
import mediapipe as mp
from tkinter import Tk, filedialog

from pathlib import Path

# Location of your AI coursework folder
folder = Path(r"C:\Users\adamb\OneDrive\Documents\AI coursework")

# Find all images in the folder
images = [
    file for file in folder.iterdir()
    if file.suffix.lower() in [".jpg", ".jpeg", ".png"]
]

print("Images found:", images)

# Check that images exist
if not images:
    raise FileNotFoundError("No images found in the folder")

# Select the first image
image_path = str(images[0])

print("Using image:", image_path)

# Load the image
image = cv2.imread(image_path)

if image is None:
    raise ValueError("Image could not be loaded")

# Step 3: Initialise MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
) as hands:

    # Convert image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Detect hand landmarks
    results = hands.process(rgb_image)

# Step 4: Extract 63 coordinates
vector = []

if results.multi_hand_landmarks:

    for landmark in results.multi_hand_landmarks[0].landmark:
        vector.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    # Draw the 21 landmarks
    mp_draw.draw_landmarks(
        image,
        results.multi_hand_landmarks[0],
        mp_hands.HAND_CONNECTIONS
    )

else:
    vector = [0.0] * 63
    print("No hand detected")

# Step 5: Display results
print("Landmark vector:", vector)
print("Number of values:", len(vector))

import matplotlib.pyplot as plt

# Convert image from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display image
plt.figure(figsize=(10, 8))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("ASL Hand Landmarks")
plt.show()

import matplotlib.pyplot as plt

# Convert image to RGB for displaying
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Display the image with hand landmarks
plt.figure(figsize=(10, 8))
plt.imshow(image_rgb)
plt.axis("off")
plt.title("ASL Hand Landmarks")
plt.show()

import numpy as np

# Convert the 63 values into a NumPy array
landmark_vector = np.array(vector, dtype=float)

# Save coordinates as a CSV file
np.savetxt(
    folder / "asl_coordinates.csv",
    landmark_vector.reshape(1, 63),
    delimiter=","
)

# Save the photograph with landmarks
cv2.imwrite(
    str(folder / "asl_landmarks.jpg"),
    image
)

print("Coordinates and image saved successfully!")