# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load raw landmarks extracted in Task 5
df = pd.read_csv("raw_landmarks.csv")
feature_cols = [col for col in df.columns if col != "label"]

print(f"Initial dataset shape: {df.shape}")
print(f"Raw feature range: min={df[feature_cols].min().min():.4f}, max={df[feature_cols].max().max():.4f}")

# 2. Data Cleaning: Remove missed-hand noise rows ([0.0] * 63) and duplicates
zero_mask = (df[feature_cols] == 0.0).all(axis=1)
print(f"Removed {zero_mask.sum()} undetected hand (all-zero) noise rows.")
df = df[~zero_mask].copy()

before_dups = len(df)
df = df.drop_duplicates().copy()
print(f"Removed {before_dups - len(df)} duplicate rows.")
print(f"Cleaned dataset shape: {df.shape}\n")

# 3. Exploratory Data Analysis: Class Distribution Bar Chart (Week 5 Lab)
class_counts = df["label"].value_counts().sort_index()
print("Class distribution after cleaning:")
print(class_counts)

plt.figure(figsize=(10, 5))
class_counts.plot(kind="bar", color="steelblue", edgecolor="black")
plt.title("ASL Sign Class Distribution (After Cleaning)")
plt.xlabel("ASL Letter")
plt.ylabel("Number of Valid Samples")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("class_distribution.png")
plt.show()

# 4. Position & Scale Normalisation + Feature Engineering
engineered_rows = []
fingertip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips

for _, row in df.iterrows():
    # Reshape 63 values into (21 landmarks, 3 coordinates)
    coords = row[feature_cols].to_numpy(dtype=float).reshape(21, 3)

    # Position invariance: shift origin to the wrist (Landmark 0)
    wrist = coords[0].copy()
    coords = coords - wrist

    # Scale invariance: divide by maximum Euclidean distance from the wrist
    max_dist = np.max(np.linalg.norm(coords, axis=1))
    if max_dist > 0:
        coords = coords / max_dist

    # Feature Engineering: Euclidean distance from wrist (0,0,0) to each of the 5 fingertips
    tip_distances = [np.linalg.norm(coords[tip_id]) for tip_id in fingertip_ids]

    # Combine 63 normalised coordinates + 5 fingertip distances + label (68 features total)
    final_row = list(coords.flatten()) + tip_distances + [row["label"]]
    engineered_rows.append(final_row)

# 5. Save cleaned & engineered dataset for Task 7 (knn.py & training_and_optimisation.py)
new_headers = feature_cols + [f"dist_tip_{i}" for i in fingertip_ids] + ["label"]
clean_df = pd.DataFrame(engineered_rows, columns=new_headers)
clean_df.to_csv("clean_features.csv", index=False)

print(f"\nSaved {clean_df.shape[0]} rows and {clean_df.shape[1] - 1} features to clean_features.csv")