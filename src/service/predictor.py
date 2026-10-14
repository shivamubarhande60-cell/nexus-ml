"""
Inference Service Engine (ML-22, ML-23).
Loads models, coordinates feature extraction, multimodal fusion, and explainability.
"""
from typing import Dict, Any, List, Optional
import os
import numpy as np
import pandas as pd
from pathlib import Path

from config import STRUCTURED_MODEL_FILE, HANDWRITING_MODEL_FILE, PREPROCESSOR_FILE
from src.features import extract_all_stroke_features
from src.data.preprocessor import ScreeningPreprocessor
from src.models.structured_model import StructuredScreeningModel
from src.models.handwriting_model import HandwritingClassifier
from src.models.fusion import MultimodalLateFusion
from src.models.explainability import ModelExplainer


class NexusPredictor:
    """
    Singleton service manager for screening inference.
    """
    def __init__(self):
        self.preprocessor: Optional[ScreeningPreprocessor] = None
        self.structured_model: Optional[StructuredScreeningModel] = None
        self.handwriting_model: Optional[HandwritingClassifier] = None
        self.fusion = MultimodalLateFusion()
        self.explainer: Optional[ModelExplainer] = None
        self.is_initialized = False

    def initialize(self):
        """
        Loads saved model artifacts from disk if available, otherwise initializes defaults.
        """
        if Path(PREPROCESSOR_FILE).exists():
            self.preprocessor = ScreeningPreprocessor.load(str(PREPROCESSOR_FILE))
        else:
            self.preprocessor = ScreeningPreprocessor()

        if Path(STRUCTURED_MODEL_FILE).exists():
            self.structured_model = StructuredScreeningModel.load(str(STRUCTURED_MODEL_FILE))
        else:
            self.structured_model = StructuredScreeningModel(model_type="rf")

        if Path(HANDWRITING_MODEL_FILE).exists():
            self.handwriting_model = HandwritingClassifier.load(str(HANDWRITING_MODEL_FILE))
        else:
            self.handwriting_model = HandwritingClassifier()

        self.explainer = ModelExplainer(
            self.structured_model,
            self.preprocessor.feature_names if self.preprocessor else []
        )
        self.is_initialized = True

    def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a full assessment payload and returns clinical screening evidence.
        """
        if not self.is_initialized:
            self.initialize()

        # 1. Feature Extraction from Raw Stroke Data (if provided)
        stroke_points = payload.get("stroke_points") or payload.get("strokes") or []
        extracted_stroke_features = {}
        data_quality = 1.0

        if stroke_points and isinstance(stroke_points, list):
            if len(stroke_points) >= 4:
                extracted_stroke_features = extract_all_stroke_features(stroke_points)
                payload["stroke_features"] = extracted_stroke_features
            else:
                data_quality = 0.20  # Insufficient strokes for motion analysis
        else:
            # If no stroke points passed directly, check if stroke_features already provided
            if not payload.get("stroke_features"):
                data_quality = 0.50

        # 2. Assemble Standard Tabular Feature Vector
        feature_df = self.preprocessor.assemble_vector(payload)

        # 3. Model Predictions
        if self.preprocessor.is_fitted and hasattr(self.structured_model.model, "classes_"):
            scaled_X = self.preprocessor.transform(feature_df)
            prob_struct = float(self.structured_model.predict_proba(scaled_X)[0, 1])
        else:
            # Calibrated fallback score based on structured benchmarks
            prob_struct = self._heuristic_structured_score(feature_df)
            scaled_X = np.zeros((1, len(feature_df.columns)))

        # Stroke kinematics score
        prob_kinematics = self._evaluate_kinematics_risk(feature_df)

        # Handwriting / Spatial score
        prob_hw = None
        if stroke_points and len(stroke_points) >= 4:
            prob_hw = self.handwriting_model.predict_proba(stroke_points)

        # 4. Multimodal Late Fusion
        task_completion = float(payload.get("task_completion_ratio", 1.0))
        fusion_result = self.fusion.evaluate_evidence(
            prob_structured=prob_struct,
            prob_kinematics=prob_kinematics,
            prob_handwriting=prob_hw,
            data_quality_score=data_quality,
            task_completion_ratio=task_completion
        )

        # 5. Explainability (Top contributing factors)
        top_factors = self.explainer.explain_instance(scaled_X, feature_df, top_k=5)

        # Combine into complete response matching SRS-6.8 & Spring Boot contract
        response = {
            "evidence_level": fusion_result["evidence_level"],
            "label": fusion_result["label"],
            "composite_score": fusion_result["composite_score"],
            "confidence": fusion_result["confidence"],
            "uncertainty": fusion_result["uncertainty"],
            "status": fusion_result["status"],
            "modality_scores": fusion_result["modality_scores"],
            "top_contributing_features": top_factors,
            "recommendation": fusion_result.get("recommendation", ""),
            "extracted_stroke_metrics": extracted_stroke_features if extracted_stroke_features else None
        }
        return response

    def _heuristic_structured_score(self, df: pd.DataFrame) -> float:
        """
        Clinical rule-based baseline probability if pre-trained weights are initializing.
        """
        score = 0.20
        phon_acc = df["phonology_accuracy"].values[0]
        if not np.isnan(phon_acc):
            if phon_acc < 0.60:
                score += 0.35
            elif phon_acc < 0.75:
                score += 0.15

        read_acc = df["reading_accuracy"].values[0]
        if not np.isnan(read_acc) and read_acc < 0.65:
            score += 0.25

        lat = df["phonology_latency_ms"].values[0]
        if not np.isnan(lat) and lat > 2000:
            score += 0.15

        return float(np.clip(score, 0.05, 0.95))

    def _evaluate_kinematics_risk(self, df: pd.DataFrame) -> float:
        """
        Scores fine-motor and kinematic irregularity.
        """
        score = 0.20
        jerk = df["normalized_jerk"].values[0]
        if not np.isnan(jerk) and jerk > 45.0:
            score += 0.30

        pause = df["pause_rate_per_sec"].values[0]
        if not np.isnan(pause) and pause > 0.50:
            score += 0.25

        drift = df["baseline_drift_degrees"].values[0]
        if not np.isnan(drift) and drift > 6.0:
            score += 0.15

        return float(np.clip(score, 0.05, 0.95))
