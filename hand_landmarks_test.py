import os
import mediapipe as mp
import cv2
import pickle

mp_hands = mp.solutions.hands 
hand = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

Data_path = "./Datasets"

data = []
labels = []

for folder in os.listdir(Data_path):
    folder_path = os.path.join(Data_path, folder)
    
    # Skip if it's not a folder (e.g. a hidden system file)
    if not os.path.isdir(folder_path):
        continue

    print(f"Processing folder: {folder}...")

    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)

        if img is None:
            print(f"Failed to read image: {img_path}")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hand.process(img_rgb)

        if results.multi_hand_landmarks:
            land_marks = results.multi_hand_landmarks[0]

            y_coords = []
            x_coords = []
            normalised_landmarks = []

            for landmark in land_marks.landmark:
                y_coords.append(landmark.y)
                x_coords.append(landmark.x)

            for landmark in land_marks.landmark:
                normalised_landmarks.append(landmark.x - min(x_coords))
                normalised_landmarks.append(landmark.y - min(y_coords))

            data.append(normalised_landmarks)
            labels.append(folder)
        else:
            print(f"No hand detected in: {img_path}")

with open("hand_landmarks.pkl", "wb") as f:
    pickle.dump((data, labels), f)

print("\n--- Summary ---")
print(f"Total hands extracted: {len(data)}")
print(f"Labels found: {set(labels)}")
if len(data) > 0:
    print(f"Features per hand (should be 42): {len(data[0])}")
print("Hand landmarks data saved to hand_landmarks.pkl")