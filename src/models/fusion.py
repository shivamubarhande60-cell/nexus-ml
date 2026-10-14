"""
Multimodal Late Fusion & Uncertainty Estimation Engine (ML-15, ML-17).
Combines structured data, handwriting dynamics, and stroke kinematics with clinical fallback logic.
"""
from typing import Dict, Any, List, Optional, Tuple
import numpy as np


class MultimodalLateFusion:
    """
    Performs calibrated late fusion across 3 screening modalities:
      1. Structured Tasks (phonology, rapid naming, decoding, working memory)
      2. Stroke Kinematics (velocity, jerk, pauses, pen-lifts, pressure)
      3. Handwriting / Spatial Tracing (density, aspect, tremor, loop completion)

    Also estimates uncertainty and evaluates data sufficiency criteria (SRS-6.6).
    """
    def __init__(
        self,
        weight_structured: float = 0.50,
        weight_kinematics: float = 0.30,
        weight_handwriting: float = 0.20
    ):
        self.w_struct = weight_structured
        self.w_kin = weight_kinematics
        self.w_hw = weight_handwriting

    def evaluate_evidence(
        self,
        prob_structured: float,
        prob_kinematics: float,
        prob_handwriting: Optional[float] = None,
        data_quality_score: float = 1.0,
        task_completion_ratio: float = 1.0
    ) -> Dict[str, Any]:
        """
        Integrates modality probabilities, computes uncertainty, and assigns evidence category.
        """
        # Fallback Check: Insufficient Evidence (ML-17 / SRS-6.6)
        if task_completion_ratio < 0.40 or data_quality_score < 0.30:
            return {
                "evidence_level": "INSUFFICIENT_EVIDENCE",
                "label": "Insufficient Evidence",
                "composite_score": 0.0,
                "confidence": 0.0,
                "uncertainty": 1.0,
                "modality_scores": {
                    "structured_tasks": round(prob_structured, 3),
                    "stroke_kinematics": round(prob_kinematics, 3),
                    "handwriting_tracing": round(prob_handwriting, 3) if prob_handwriting is not None else None
                },
                "status": "FALLBACK",
                "reason": "Incomplete task data or insufficient stroke duration for clinical assessment."
            }

        # Handle missing handwriting modality gracefully
        if prob_handwriting is None:
            w_total = self.w_struct + self.w_kin
            norm_w_struct = self.w_struct / w_total
            norm_w_kin = self.w_kin / w_total
            composite = (prob_structured * norm_w_struct) + (prob_kinematics * norm_w_kin)
            modality_probs = [prob_structured, prob_kinematics]
        else:
            composite = (
                prob_structured * self.w_struct +
                prob_kinematics * self.w_kin +
                prob_handwriting * self.w_hw
            )
            modality_probs = [prob_structured, prob_kinematics, prob_handwriting]

        # Uncertainty: Combination of cross-modality divergence and binary prediction entropy
        cross_modality_std = float(np.std(modality_probs))
        p = np.clip(composite, 1e-5, 1 - 1e-5)
        binary_entropy = float(-(p * np.log2(p) + (1 - p) * np.log2(1 - p)))
        
        # Combined uncertainty scaled to [0, 1]
        raw_uncertainty = (cross_modality_std * 1.5) + (binary_entropy * 0.3) + ((1.0 - data_quality_score) * 0.4)
        uncertainty = float(np.clip(raw_uncertainty, 0.05, 0.95))
        confidence = float(np.round(1.0 - uncertainty, 3))

        # Assign standard 4-tier screening category (SRS-6.8)
        composite_score = float(np.round(composite, 3))

        if composite_score >= 0.70:
            evidence_level = "ELEVATED_CONCERN"
            label = "Elevated Concern"
            recommendation = "Referral for detailed clinical evaluation by licensed developmental specialist."
        elif composite_score >= 0.45:
            evidence_level = "SUPPORTING_EVIDENCE"
            label = "Supporting Evidence"
            recommendation = "Targeted classroom learning support; re-screen in 6-8 weeks."
        elif composite_score >= 0.25:
            evidence_level = "DEVELOPING"
            label = "Developing"
            recommendation = "Age-appropriate developmental variation; continue routine classroom observation."
        else:
            evidence_level = "MONITOR"
            label = "Monitor"
            recommendation = "Profile shows typical developmental indicators across tested modalities."

        return {
            "evidence_level": evidence_level,
            "label": label,
            "composite_score": composite_score,
            "confidence": confidence,
            "uncertainty": float(np.round(uncertainty, 3)),
            "modality_scores": {
                "structured_tasks": float(np.round(prob_structured, 3)),
                "stroke_kinematics": float(np.round(prob_kinematics, 3)),
                "handwriting_tracing": float(np.round(prob_handwriting, 3)) if prob_handwriting is not None else None
            },
            "recommendation": recommendation,
            "status": "VALID"
        }
