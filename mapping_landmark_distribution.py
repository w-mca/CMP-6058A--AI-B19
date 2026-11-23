# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load raw landmarks (Week 5 lab pandas approach)
df = pd.read_csv("raw_landmarks.csv")
print("Initial dataset shape:", df.shape)

# 2. Data Cleaning: Remove noise (all-zero rows) and duplicates
feature_cols = [col for col in df.columns if col != "label"]

noise_mask = (df[feature_cols] == 0.0).all(axis=1)
print(f"Noise rows (undetected hands) removed: {noise_mask.sum()}")
df = df[~noise_mask].copy()

before_dups = len(df)
df = df.drop_duplicates().copy()
print(f"Duplicate rows removed: {before_dups - len(df)}")

# 3. Data Analysis & Visualisation: Feature ranges & class distribution
print("\nFeature value range (before normalisation):")
print(f"Min: {df[feature_cols].min().min():.4f}, Max: {df[feature_cols].max().max():.4f}")

class_counts = df["label"].value_counts().sort_index()
print("\nClass distribution:")
print(class_counts)

plt.figure(figsize=(10, 5))
class_counts.plot(kind="bar", rot=0, color="steelblue")
plt.title("ASL Dataset Class Distribution (After Cleaning)")
plt.xlabel("ASL Letter")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("class_distribution.png")
plt.show()

# --- PART B: POSITION/SCALE NORMALISATION & FEATURE ENGINEERING ---
engineered_rows = []
fingertip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky tips

for _, row in df.iterrows():
    coords = row[feature_cols].to_numpy(dtype=float).reshape(21, 3)

    # Shift origin to wrist (Landmark 0) -> position invariance
    wrist = coords[0].copy()
    coords = coords - wrist

    # Scale by max distance from wrist -> scale invariance
    max_dist = np.max(np.linalg.norm(coords, axis=1))
    if max_dist > 0:
        coords = coords / max_dist

    # Feature engineering: Euclidean distance from wrist to each of the 5 fingertips
    tip_distances = [np.linalg.norm(coords[tip_id]) for tip_id in fingertip_ids]

    final_row = list(coords.flatten()) + tip_distances + [row["label"]]
    engineered_rows.append(final_row)

new_headers = feature_cols + [f"dist_tip_{i}" for i in fingertip_ids] + ["label"]
clean_df = pd.DataFrame(engineered_rows, columns=new_headers)
clean_df.to_csv("clean_features.csv", index=False)

print(f"\nSaved {clean_df.shape[0]} rows and {clean_df.shape[1] - 1} features to clean_features.csv")