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
