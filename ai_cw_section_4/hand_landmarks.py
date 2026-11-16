# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import os
import csv
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hand = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)

Data_path = "./Datasets" ###change this to google drive path to access the dataset
rows = []

for folder in os.listdir(Data_path):
    folder_path = os.path.join(Data_path, folder)
    if not os.path.isdir(folder_path):
        continue

    print(f"Processing folder: {folder}...")

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hand.process(img_rgb)

        if results.multi_hand_landmarks:
            landmarks = results.multi_hand_landmarks[0]
            vector = []
            for lm in landmarks.landmark:
                vector.extend([lm.x, lm.y, lm.z])
        else:
            # Task 5 rule: set 63 values to zero when no hand is detected
            vector = [0.0] * 63

        rows.append(vector + [folder])

# Build column headers: x0, y0, z0 ... x20, y20, z20, label
headers = []
for i in range(21):
    headers.extend([f"x{i}", f"y{i}", f"z{i}"])
headers.append("label")

with open("raw_landmarks.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"\nSaved {len(rows)} rows (63 features + label) to raw_landmarks.csv")