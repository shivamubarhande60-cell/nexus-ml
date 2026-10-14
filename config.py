"""
Configuration settings for the Nexus AI/ML Screening Intelligence Service.
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "saved_models"
DATA_DIR = BASE_DIR / "data"

# Ensure runtime directories exist
MODELS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Model Artifact Filenames
STRUCTURED_MODEL_FILE = MODELS_DIR / "nexus_structured_model.pkl"
HANDWRITING_MODEL_FILE = MODELS_DIR / "nexus_handwriting_model.pkl"
PREPROCESSOR_FILE = MODELS_DIR / "nexus_preprocessor.pkl"

# Service Configuration
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
DEBUG_MODE = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")

# Evidence Level Thresholds
# Standard 4-tier screening evidence categories defined in SRS-6.8
EVIDENCE_LEVELS = {
    "ELEVATED_CONCERN": {"min_score": 0.70, "label": "Elevated Concern", "color": "RED"},
    "SUPPORTING_EVIDENCE": {"min_score": 0.45, "label": "Supporting Evidence", "color": "ORANGE"},
    "DEVELOPING": {"min_score": 0.25, "label": "Developing", "color": "YELLOW"},
    "MONITOR": {"min_score": 0.00, "label": "Monitor", "color": "GREEN"},
}

# Data Quality & Fallback Thresholds (SRS-6.6 / ML-17)
MIN_REQUIRED_STROKES = 10
MIN_TASK_COMPLETION_RATIO = 0.50
UNCERTAINTY_THRESHOLD = 0.35  # High disagreement across modalities triggers uncertainty flag

# Age Bands (SRS-4.2)
AGE_BANDS = ["5-7", "6-8", "8-10", "10-12"]
