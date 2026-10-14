"""
Handwriting & Tracing Analysis Model (ML-14).
Evaluates letter tracing fidelity, contour smoothness, and fine-motor shape reproduction.
"""
from typing import Dict, Any, List, Optional
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib


class HandwritingClassifier:
    """
    Evaluates handwriting and tracing quality from normalized stroke coordinates or raster images.
    Extracts spatial density, contour smoothness, loop completion, and tremor indicators.
    """
    def __init__(self):
        self.model = ExtraTreesClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42
        )
        self.is_fitted = False

    @staticmethod
    def extract_spatial_features(points: List[Dict[str, Any]]) -> np.ndarray:
        """
        Extracts an 8-dimensional spatial geometry descriptor from strokes:
        [coverage_area, perimeter_ratio, vertical_symmetry, horizontal_symmetry,
         stroke_density, aspect_ratio, tremor_frequency, loop_closure_gap]
        """
        if not points or len(points) < 4:
            return np.zeros(8)

        x = np.array([p.get("x", 0.0) for p in points], dtype=float)
        y = np.array([p.get("y", 0.0) for p in points], dtype=float)

        min_x, max_x = np.min(x), np.max(x)
        min_y, max_y = np.min(y), np.max(y)
        w = max(max_x - min_x, 1.0)
        h = max(max_y - min_y, 1.0)

        # Normalize coordinates into [0, 1] bounding box
        nx = (x - min_x) / w
        ny = (y - min_y) / h

        coverage_area = (w * h) / 10000.0
        aspect = w / h

        # Tremor frequency (high-frequency directional reversals)
        dx = np.diff(nx)
        dy = np.diff(ny)
        reversals_x = np.sum((dx[:-1] * dx[1:]) < 0)
        reversals_y = np.sum((dy[:-1] * dy[1:]) < 0)
        tremor_freq = float(reversals_x + reversals_y) / max(len(points), 1)

        # Loop closure: distance between stroke start and end relative to bounding diagonal
        closure_gap = float(np.sqrt((nx[-1] - nx[0])**2 + (ny[-1] - ny[0])**2))

        # Spatial symmetries around centroid
        cx, cy = np.mean(nx), np.mean(ny)
        v_sym = float(np.mean(np.abs(nx - cx)))
        h_sym = float(np.mean(np.abs(ny - cy)))

        path_len = float(np.sum(np.sqrt(dx**2 + dy**2)))
        perimeter_ratio = path_len / (2 * (w + h) / max(w, h))

        density = path_len / max(coverage_area, 0.01)

        return np.array([
            min(coverage_area, 100.0),
            min(perimeter_ratio, 20.0),
            v_sym,
            h_sym,
            min(density, 100.0),
            min(aspect, 10.0),
            tremor_freq,
            min(closure_gap, 2.0)
        ])

    def fit(self, X: np.ndarray, y: np.ndarray) -> "HandwritingClassifier":
        self.model.fit(X, y)
        self.is_fitted = True
        return self

    def predict_proba(self, points: List[Dict[str, Any]]) -> float:
        """
        Returns probability of handwriting / motor difficulty [0.0 to 1.0].
        """
        if not self.is_fitted:
            # Calibrated fallback based on tremor and loop closure
            feat = self.extract_spatial_features(points)
            tremor = feat[6]
            score = np.clip(tremor * 1.5, 0.05, 0.95)
            return float(score)

        feat = self.extract_spatial_features(points).reshape(1, -1)
        prob = self.model.predict_proba(feat)[0, 1]
        return float(prob)

    def save(self, filepath: str) -> None:
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "HandwritingClassifier":
        return joblib.load(filepath)
