"""
Feature Vector Assembly and Preprocessing Pipeline (ML-09, ML-10).
Handles feature mapping, missing value imputation, scaling, and validation.
"""
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib


FEATURE_COLUMNS = [
    "age_years",
    "grade",
    "phonology_accuracy",
    "phonology_latency_ms",
    "rapid_naming_speed",
    "reading_accuracy",
    "working_memory_score",
    "mean_velocity",
    "normalized_jerk",
    "pen_lift_count",
    "in_air_ratio",
    "pause_rate_per_sec",
    "mean_pressure",
    "pressure_std",
    "tortuosity",
    "baseline_drift_degrees"
]


class ScreeningPreprocessor:
    """
    Standard preprocessor for screening feature vectors.
    Imputes missing task signals with age-band median values and normalizes with StandardScaler.
    """
    def __init__(self):
        self.imputer = SimpleImputer(strategy="median")
        self.scaler = StandardScaler()
        self.feature_names = FEATURE_COLUMNS
        self.is_fitted = False

    def fit(self, X: pd.DataFrame) -> "ScreeningPreprocessor":
        features = X[self.feature_names].copy()
        imputed = self.imputer.fit_transform(features)
        self.scaler.fit(imputed)
        self.is_fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise ValueError("ScreeningPreprocessor must be fitted before calling transform.")
        features = X[self.feature_names].copy()
        imputed = self.imputer.transform(features)
        scaled = self.scaler.transform(imputed)
        return scaled

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.fit(X).transform(X)

    def assemble_vector(self, raw_input: Dict[str, Any]) -> pd.DataFrame:
        """
        Converts unstructured raw API payload (with nested stroke features or task lists)
        into the standardized tabular feature format.
        """
        row = {}
        # Demographic
        row["age_years"] = float(raw_input.get("age_years", 7.0))
        row["grade"] = float(raw_input.get("grade", max(1, int(row["age_years"] - 5))))

        # Structured tasks
        row["phonology_accuracy"] = float(raw_input.get("phonology_accuracy", np.nan))
        row["phonology_latency_ms"] = float(raw_input.get("phonology_latency_ms", np.nan))
        row["rapid_naming_speed"] = float(raw_input.get("rapid_naming_speed", np.nan))
        row["reading_accuracy"] = float(raw_input.get("reading_accuracy", np.nan))
        row["working_memory_score"] = float(raw_input.get("working_memory_score", np.nan))

        # Kinematics & Stroke features (may be nested inside 'stroke_features' or at root)
        stroke_data = raw_input.get("stroke_features", {})
        row["mean_velocity"] = float(stroke_data.get("mean_velocity", raw_input.get("mean_velocity", np.nan)))
        row["normalized_jerk"] = float(stroke_data.get("normalized_jerk", raw_input.get("normalized_jerk", np.nan)))
        row["pen_lift_count"] = float(stroke_data.get("pen_lift_count", raw_input.get("pen_lift_count", np.nan)))
        row["in_air_ratio"] = float(stroke_data.get("in_air_ratio", raw_input.get("in_air_ratio", np.nan)))
        row["pause_rate_per_sec"] = float(stroke_data.get("pause_rate_per_sec", raw_input.get("pause_rate_per_sec", np.nan)))
        row["mean_pressure"] = float(stroke_data.get("mean_pressure", raw_input.get("mean_pressure", np.nan)))
        row["pressure_std"] = float(stroke_data.get("pressure_std", raw_input.get("pressure_std", np.nan)))
        row["tortuosity"] = float(stroke_data.get("tortuosity", raw_input.get("tortuosity", np.nan)))
        row["baseline_drift_degrees"] = float(stroke_data.get("baseline_drift_degrees", raw_input.get("baseline_drift_degrees", np.nan)))

        return pd.DataFrame([row], columns=self.feature_names)

    def save(self, filepath: str) -> None:
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "ScreeningPreprocessor":
        return joblib.load(filepath)
