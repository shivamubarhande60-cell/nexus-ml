"""
Model Training and Evaluation Pipeline (ML-11, ML-12, ML-13, ML-18, ML-19).
Trains Random Forest, Gradient Boosting, and Handwriting classifiers; outputs benchmark comparison.
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

from config import STRUCTURED_MODEL_FILE, HANDWRITING_MODEL_FILE, PREPROCESSOR_FILE, DATA_DIR
from src.data.generator import generate_synthetic_screening_dataset
from src.data.preprocessor import ScreeningPreprocessor, FEATURE_COLUMNS
from src.models.structured_model import StructuredScreeningModel
from src.models.handwriting_model import HandwritingClassifier


def run_training_pipeline():
    print("=" * 60)
    print("      NEXUS AI/ML: MODEL TRAINING & BENCHMARK PIPELINE      ")
    print("=" * 60)

    # 1. Generate/Load Dataset (ML-05)
    print("\n[Step 1/5] Generating clinically grounded screening dataset...")
    df = generate_synthetic_screening_dataset(n_samples=2000, random_seed=42)
    data_path = DATA_DIR / "nexus_synthetic_screening_dataset.csv"
    df.to_csv(data_path, index=False)
    print(f" -> Dataset saved to {data_path} ({len(df)} samples, {len(df.columns)} columns)")

    # 2. Fit Preprocessor (ML-09, ML-10)
    print("\n[Step 2/5] Fitting Feature Vector Preprocessor & Scaler...")
    preprocessor = ScreeningPreprocessor()
    X_scaled = preprocessor.fit_transform(df)
    y = df["screening_label"].values
    preprocessor.save(str(PREPROCESSOR_FILE))
    print(f" -> Preprocessor saved to {PREPROCESSOR_FILE}")

    # 3. Train & Compare Models (ML-11, ML-12, ML-13)
    print("\n[Step 3/5] Training Classifiers: Random Forest vs. Gradient Boosting...")
    rf_model = StructuredScreeningModel(model_type="rf")
    rf_metrics = rf_model.train_and_evaluate(X_scaled, y, feature_names=FEATURE_COLUMNS)

    gb_model = StructuredScreeningModel(model_type="gb")
    gb_metrics = gb_model.train_and_evaluate(X_scaled, y, feature_names=FEATURE_COLUMNS)

    print("\n" + "-" * 50)
    print(f"{'Metric':<18} | {'Random Forest':<15} | {'Gradient Boosting':<15}")
    print("-" * 50)
    for m in ["accuracy", "precision", "recall", "f1_score", "roc_auc"]:
        print(f"{m.capitalize():<18} | {rf_metrics[m]:<15.4f} | {gb_metrics[m]:<15.4f}")
    print("-" * 50)

    # Select champion model based on F1-score
    if rf_metrics["f1_score"] >= gb_metrics["f1_score"]:
        champion = rf_model
        champion_name = "Random Forest"
    else:
        champion = gb_model
        champion_name = "Gradient Boosting"

    print(f"\n -> Selected Champion Structured Model: {champion_name}")
    champion.save(str(STRUCTURED_MODEL_FILE))
    print(f" -> Saved to {STRUCTURED_MODEL_FILE}")

    # Top Feature Importances (ML-16)
    print("\nTop 5 Contributing Features:")
    for feat, imp in list(champion.get_feature_importances().items())[:5]:
        print(f"   * {feat:<25}: {imp * 100:.2f}%")

    # 4. Train Handwriting Model (ML-14)
    print("\n[Step 4/5] Training Handwriting & Tracing Spatial Classifier...")
    hw_classifier = HandwritingClassifier()
    # Synthesize spatial stroke features for handwriting training
    n_hw = 1000
    np.random.seed(42)
    hw_X = np.random.uniform(0.1, 1.0, size=(n_hw, 8))
    hw_y = np.random.choice([0, 1], size=n_hw, p=[0.6, 0.4])
    hw_classifier.fit(hw_X, hw_y)
    hw_classifier.save(str(HANDWRITING_MODEL_FILE))
    print(f" -> Handwriting model saved to {HANDWRITING_MODEL_FILE}")

    # 5. Write Evaluation Report (ML-19)
    print("\n[Step 5/5] Writing Model Evaluation Report (ML-19)...")
    report_file = Path(__file__).resolve().parent / "docs" / "MODEL_EVALUATION_REPORT.md"
    report_content = f"""# Nexus AI/ML - Model Evaluation Report (ML-19)
**Author:** Aarohi Wagh (Lead ML Developer)  
**Date:** October 2026  
**System:** Nexus Screening Intelligence Service (ASD/LD Screening)

---

## 1. Executive Summary
This report summarizes the comparative evaluation between **Random Forest** and **Gradient Boosting** algorithms for the multimodal developmental screening pipeline.

## 2. Benchmark Metrics Comparison

| Metric | Random Forest Classifier | Gradient Boosting Classifier | Winner |
|---|---|---|---|
| **Accuracy** | {rf_metrics['accuracy']:.4f} | {gb_metrics['accuracy']:.4f} | {"Random Forest" if rf_metrics['accuracy'] >= gb_metrics['accuracy'] else "Gradient Boosting"} |
| **Precision** | {rf_metrics['precision']:.4f} | {gb_metrics['precision']:.4f} | {"Random Forest" if rf_metrics['precision'] >= gb_metrics['precision'] else "Gradient Boosting"} |
| **Recall (Sensitivity)** | {rf_metrics['recall']:.4f} | {gb_metrics['recall']:.4f} | {"Random Forest" if rf_metrics['recall'] >= gb_metrics['recall'] else "Gradient Boosting"} |
| **F1-Score** | {rf_metrics['f1_score']:.4f} | {gb_metrics['f1_score']:.4f} | **{champion_name}** |
| **ROC-AUC** | {rf_metrics['roc_auc']:.4f} | {gb_metrics['roc_auc']:.4f} | {"Random Forest" if rf_metrics['roc_auc'] >= gb_metrics['roc_auc'] else "Gradient Boosting"} |

## 3. Top Contributing Clinical Biomarkers
Feature importance ranking extracted from the champion model:

"""
    for feat, imp in list(champion.get_feature_importances().items())[:7]:
        report_content += f"- **`{feat}`**: {imp * 100:.2f}%\n"

    report_content += """
## 4. Multimodal Fusion & Uncertainty Logic
- Late fusion weights: Structured (50%), Kinematics (30%), Handwriting (20%).
- Fallback trigger: Returns `INSUFFICIENT_EVIDENCE` when completed tasks < 40% or stroke count < 10.
- 4-Tier Evidence levels: `Elevated Concern`, `Supporting Evidence`, `Developing`, `Monitor`.
"""
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f" -> Evaluation report saved to {report_file}")
    print("\n[SUCCESS] Model training and evaluation complete!")


if __name__ == "__main__":
    run_training_pipeline()
