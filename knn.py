# Group number: B19
# Student IDs: 100437354, Churchill, Adam
# Student IDs: 100463731, Emeka-Ugwuadu, Sean
# Student IDs: 100436949, McAlister, William

import math
from collections import Counter


class KNNClassifier:
    """From-scratch k-Nearest Neighbours classifier using only Python standard libraries."""

    def __init__(self, k=3):
        self.k = k
        self.X_train = []
        self.y_train = []

    def fit(self, X, y):
        # Convert inputs to standard Python lists in case numpy arrays are passed in
        self.X_train = [list(row) for row in X]
        self.y_train = list(y)
        return self

    def _euclidean_distance(self, point1, point2):
        total = 0.0
        for a, b in zip(point1, point2):
            diff = a - b
            total += diff * diff
        return math.sqrt(total)

    def predict_one(self, x):
        distances = []
        for train_x, train_y in zip(self.X_train, self.y_train):
            dist = self._euclidean_distance(x, train_x)
            distances.append((dist, train_y))

        # Sort by distance ascending and take the k nearest labels
        distances.sort(key=lambda pair: pair[0])
        k_nearest_labels = [label for _, label in distances[:self.k]]

        # Return the most common label among the k neighbours
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def predict(self, X):
        return [self.predict_one(list(row)) for row in X]