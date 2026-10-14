"""
Structured ML Models: Random Forest & Gradient Boosting (ML-11, ML-12, ML-13, ML-18).
Implements model training, cross-validation, comparison, and serialization.
"""
from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib


class StructuredScreeningModel:
    """
    Supervised classifier ensemble for structured task and kinematics screening.
    Supports Random Forest and Gradient Boosting.
    """
    def __init__(self, model_type: str = "rf"):
        self.model_type = model_type.lower()
        if self.model_type == "rf":
            self.model = RandomForestClassifier(
                n_estimators=150,
                max_depth=8,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight="balanced",
                random_state=42
            )
        elif self.model_type in ["gb", "xgboost"]:
            self.model = GradientBoostingClassifier(
                n_estimators=120,
                learning_rate=0.08,
                max_depth=5,
                subsample=0.85,
                random_state=42
            )
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

        self.metrics = {}
        self.feature_names = []

    def train_and_evaluate(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: list,
        test_size: float = 0.20
    ) -> Dict[str, float]:
        self.feature_names = feature_names
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )

        self.model.fit(X_train, y_train)

        # Predictions
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]

        self.metrics = {
            "accuracy": round(float(accuracy_score(y_test, y_pred)), 4),
            "precision": round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, y_pred)), 4),
            "f1_score": round(float(f1_score(y_test, y_pred)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, y_prob)), 4)
        }
        return self.metrics

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict_proba(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def get_feature_importances(self) -> Dict[str, float]:
        if not hasattr(self.model, "feature_importances_"):
            return {}
        importances = self.model.feature_importances_
        return {
            name: round(float(imp), 4)
            for name, imp in sorted(zip(self.feature_names, importances), key=lambda x: x[1], reverse=True)
        }

    def save(self, filepath: str) -> None:
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "StructuredScreeningModel":
        return joblib.load(filepath)
