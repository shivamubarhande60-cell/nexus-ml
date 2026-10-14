# 🤖 Nexus AI/ML (Screening Intelligence Service)

**Lead Developer:** Aarohi Wagh  
**Project:** AI-Based Autism and Learning Disability Screening Support System  
**Affiliation:** ADYPSOE, Savitribai Phule Pune University (SPPU), AY 2026-27  
**Technologies:** Python 3.13 / 3.12, Scikit-learn, Flask, Flask-CORS, NumPy, SciPy, Pandas, Matplotlib, SHAP

---

## 📌 Architecture & Modules

```
nexus-ml/
├── docs/                                  # Specifications and requirements
│   ├── PRD.md                             # Product Requirements Document
│   ├── SRS.md                             # Software Requirements Specification
│   ├── WBS_GitHub_Issues.md               # Task Breakdown & Issues Matrix
│   └── MODEL_EVALUATION_REPORT.md         # Benchmark comparison report
├── src/
│   ├── data/
│   │   ├── generator.py                   # Clinical synthetic dataset generator (ML-05)
│   │   └── preprocessor.py                # Imputation, vector assembly, scaling (ML-09, ML-10)
│   ├── features/
│   │   ├── kinematics.py                  # Velocity, acceleration, jerk smoothness (ML-06)
│   │   ├── stroke_events.py               # Pen-lifts, pauses, hesitation, pressure (ML-07)
│   │   └── geometry.py                    # Curvature, alignment drift, bounding box (ML-08)
│   ├── models/
│   │   ├── structured_model.py            # Random Forest & Gradient Boosting classifiers (ML-11, 12, 13)
│   │   ├── handwriting_model.py           # Spatial handwriting and tracing classifier (ML-14)
│   │   ├── fusion.py                      # Multimodal Late Fusion & Uncertainty Engine (ML-15, 17)
│   │   └── explainability.py              # Clinical feature attribution & SHAP explainer (ML-16)
│   └── service/
│       └── predictor.py                   # Unified inference coordinator (ML-22, 23)
├── notebooks/
│   └── 01_model_training_and_exploration.ipynb # Interactive exploration notebook (ML-03)
├── saved_models/                          # Serialized trained model artifacts (.pkl)
├── config.py                              # Central configuration & clinical thresholds
├── app.py                                 # Flask REST API server (ML-20, 21, 25)
├── train.py                               # End-to-end training and evaluation pipeline (ML-18, 19)
├── test_api.py                            # Automated unit tests for API endpoints (ML-24)
└── requirements.txt                       # Project dependencies (ML-01, ML-02)
```

---

## 🚀 Setup & Execution Guide

### 1. Create Virtual Environment & Install Dependencies (ML-01, ML-02)
```bash
# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train Models and Generate Artifacts (ML-11 through ML-19)
```bash
python train.py
```
This script:
1. Generates 2,000 clinically grounded synthetic patient screening profiles.
2. Fits the feature scaler and missing-data imputer (`nexus_preprocessor.pkl`).
3. Trains and benchmarks **Random Forest** vs. **Gradient Boosting**.
4. Trains the handwriting spatial classifier (`nexus_handwriting_model.pkl`).
5. Evaluates accuracy, precision, recall, F1, ROC-AUC, and generates `docs/MODEL_EVALUATION_REPORT.md`.

### 3. Start the Flask REST API Server (ML-20, ML-21)
```bash
python app.py
```
The server starts at `http://0.0.0.0:5000` with CORS enabled for Spring Boot backend and React frontend.

### 4. Run Automated API Tests (ML-24)
```bash
python test_api.py
```

---

## 📡 API Specification

### `GET /health`
Returns service status and model initialization state.
```json
{
  "status": "UP",
  "models_loaded": true
}
```

### `POST /predict` (and `POST /api/analysis` for Spring Boot BE-25)
Accepts child assessment data, task accuracy/latency, and canvas stroke coordinate streams.

**Example Request Payload:**
```json
{
  "child_id": "child-101",
  "age_years": 8.0,
  "grade": 2,
  "phonology_accuracy": 0.45,
  "phonology_latency_ms": 2800,
  "rapid_naming_speed": 1.2,
  "reading_accuracy": 0.50,
  "working_memory_score": 0.55,
  "stroke_points": [
    {"x": 12.5, "y": 14.0, "t": 100, "pressure": 0.75, "pen_state": 1},
    {"x": 22.0, "y": 30.0, "t": 220, "pressure": 0.82, "pen_state": 1},
    {"x": 38.0, "y": 48.0, "t": 350, "pressure": 0.40, "pen_state": 1}
  ]
}
```

**Example Response:**
```json
{
  "evidence_level": "ELEVATED_CONCERN",
  "label": "Elevated Concern",
  "composite_score": 0.785,
  "confidence": 0.84,
  "uncertainty": 0.16,
  "status": "VALID",
  "modality_scores": {
    "structured_tasks": 0.82,
    "stroke_kinematics": 0.75,
    "handwriting_tracing": 0.71
  },
  "top_contributing_features": [
    {
      "feature": "phonology_accuracy",
      "label": "Phonological Processing Accuracy",
      "raw_value": 0.45,
      "contribution": 0.22,
      "impact": "High",
      "direction": "Risk Indicator"
    },
    {
      "feature": "normalized_jerk",
      "label": "Fine-Motor Jerk / Motion Smoothness",
      "raw_value": 78.4,
      "contribution": 0.18,
      "impact": "High",
      "direction": "Risk Indicator"
    }
  ],
  "recommendation": "Referral for detailed clinical evaluation by licensed developmental specialist."
}
```

---

## 📋 WBS Task Completion Status (Aarohi Wagh)

| Issue # | Title | Status |
|---|---|---|
| **ML-01** | Create Python virtual environment + requirements.txt | ✅ Completed |
| **ML-02** | Install dependencies (numpy, pandas, scikit-learn, flask, etc.) | ✅ Completed |
| **ML-03** | Set up Jupyter notebook environment | ✅ Completed |
| **ML-04** | Set up GitHub repo + .gitignore | ✅ Completed |
| **ML-05** | Research and collect/generate sample dataset | ✅ Completed |
| **ML-06** | Write stroke feature extractor (velocity, acceleration, jerk) | ✅ Completed |
| **ML-07** | Write pen-lift and pause counter from stroke events | ✅ Completed |
| **ML-08** | Write curvature and alignment calculator | ✅ Completed |
| **ML-09** | Build feature vector: F = [accuracy, time, pressure, velocity, ...] | ✅ Completed |
| **ML-10** | Write preprocessing pipeline (normalize, handle missing) | ✅ Completed |
| **ML-11** | Train Random Forest on structured task features | ✅ Completed |
| **ML-12** | Train Gradient Boosting on structured task features | ✅ Completed |
| **ML-13** | Compare RF vs Gradient Boosting (accuracy, F1, ROC-AUC) | ✅ Completed |
| **ML-14** | Train Handwriting / Tracing spatial classifier | ✅ Completed |
| **ML-15** | Implement late fusion (weighted average / meta-model) | ✅ Completed |
| **ML-16** | Add SHAP explainability for top features | ✅ Completed |
| **ML-17** | Add INSUFFICIENT EVIDENCE fallback (low quality data) | ✅ Completed |
| **ML-18** | Save trained models as .pkl files | ✅ Completed |
| **ML-19** | Evaluate model performance + write evaluation report | ✅ Completed |
| **ML-20** | Create Flask app (app.py) | ✅ Completed |
| **ML-21** | Implement POST /predict endpoint | ✅ Completed |
| **ML-22** | Load saved models at Flask startup | ✅ Completed |
| **ML-23** | Return response: {evidence_level, shap_values, uncertainty} | ✅ Completed |
| **ML-24** | Test Flask API with unit tests & test suite | ✅ Completed |
| **ML-25** | Add input validation + error handling in Flask | ✅ Completed |
