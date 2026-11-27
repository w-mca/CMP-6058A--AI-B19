# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import KFold, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import metrics

# Import your from-scratch k-NN classifier
from knn import KNNClassifier

SEED = 26

# 1. Load the cleaned & engineered dataset (68 features + label)
df = pd.read_csv("clean_features.csv")
X = df.drop(columns=["label"]).to_numpy(dtype=float)
y = df["label"].to_numpy()

print(f"Loaded {X.shape[0]} samples with {X.shape[1]} features across {len(np.unique(y))} classes.\n")

# Helper function to run 5-fold cross-validation manually so it works cleanly with custom KNNClassifier
def evaluate_5fold_cv(model_builder, X_data, y_data):
    kf = KFold(n_splits=5, shuffle=True, random_state=SEED)
    fold_accuracies = []

    for train_idx, val_idx in kf.split(X_data):
        X_tr, X_va = X_data[train_idx], X_data[val_idx]
        y_tr, y_va = y_data[train_idx], y_data[val_idx]

        clf = model_builder()
        clf.fit(X_tr, y_tr)
        preds = clf.predict(X_va)
        fold_accuracies.append(metrics.accuracy_score(y_va, preds))

    return np.mean(fold_accuracies), np.std(fold_accuracies)


# 2. Hyperparameter Tuning & 5-Fold CV across 3 Supervised Classifiers
results = {}

print("--- 1. From-Scratch k-NN (knn.py) ---")
for k in [1, 3, 5, 7]:
    mean_acc, std_acc = evaluate_5fold_cv(lambda k=k: KNNClassifier(k=k), X, y)
    results[f"k-NN (k={k})"] = (mean_acc, lambda k=k: KNNClassifier(k=k))
    print(f"  k={k}: 5-Fold CV Accuracy = {mean_acc * 100:.2f}% (+/- {std_acc * 100:.2f}%)")

print("\n--- 2. Decision Tree (Week 5 Lab) ---")
for depth in [5, 10, 15, None]:
    mean_acc, std_acc = evaluate_5fold_cv(
        lambda d=depth: DecisionTreeClassifier(max_depth=d, random_state=SEED), X, y
    )
    results[f"DecisionTree (depth={depth})"] = (
        mean_acc,
        lambda d=depth: DecisionTreeClassifier(max_depth=d, random_state=SEED),
    )
    print(f"  max_depth={depth}: 5-Fold CV Accuracy = {mean_acc * 100:.2f}% (+/- {std_acc * 100:.2f}%)")

print("\n--- 3. Neural Network MLP (Intro to NN Lab) ---")
for layers in [(50,), (100,), (100, 50)]:
    mean_acc, std_acc = evaluate_5fold_cv(
        lambda h=layers: MLPClassifier(hidden_layer_sizes=h, max_iter=1000, random_state=SEED), X, y
    )
    results[f"MLP {layers}"] = (
        mean_acc,
        lambda h=layers: MLPClassifier(hidden_layer_sizes=h, max_iter=1000, random_state=SEED),
    )
    print(f"  hidden_layers={layers}: 5-Fold CV Accuracy = {mean_acc * 100:.2f}% (+/- {std_acc * 100:.2f}%)")


# 3. Select the Best Model & Plot Confusion Matrix
best_name = max(results, key=lambda name: results[name][0])
best_cv_acc, best_builder = results[best_name]
print(f"\nBest Configuration: {best_name} ({best_cv_acc * 100:.2f}% 5-fold CV accuracy)")

# Holdout split for confusion matrix visualisation (matching your UEA lab sheets)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=True, random_state=SEED
)
eval_model = best_builder()
eval_model.fit(X_train, y_train)
y_pred = eval_model.predict(X_test)

fig, ax = plt.subplots(figsize=(10, 8))
metrics.ConfusionMatrixDisplay.from_predictions(y_test, y_pred, ax=ax)
ax.set_title(f"Confusion Matrix - {best_name}")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
plt.show()

# 4. Train the winning model on 100% of clean_features.csv and save for Task 8 (Live Webcam)
final_model = best_builder()
final_model.fit(X, y)
with open("best_asl_model.pkl", "wb") as f:
    pickle.dump(final_model, f)

print("Saved final trained model to best_asl_model.pkl!")