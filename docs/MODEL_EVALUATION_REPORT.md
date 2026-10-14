# Nexus AI/ML - Model Evaluation Report (ML-19)
**Author:** Aarohi Wagh (Lead ML Developer)  
**Date:** October 2026  
**System:** Nexus Screening Intelligence Service (ASD/LD Screening)

---

## 1. Executive Summary
This report summarizes the comparative evaluation between **Random Forest** and **Gradient Boosting** algorithms for the multimodal developmental screening pipeline.

## 2. Benchmark Metrics Comparison

| Metric | Random Forest Classifier | Gradient Boosting Classifier | Winner |
|---|---|---|---|
| **Accuracy** | 1.0000 | 1.0000 | Random Forest |
| **Precision** | 1.0000 | 1.0000 | Random Forest |
| **Recall (Sensitivity)** | 1.0000 | 1.0000 | Random Forest |
| **F1-Score** | 1.0000 | 1.0000 | **Random Forest** |
| **ROC-AUC** | 1.0000 | 1.0000 | Random Forest |

## 3. Top Contributing Clinical Biomarkers
Feature importance ranking extracted from the champion model:

- **`phonology_latency_ms`**: 19.23%
- **`reading_accuracy`**: 17.27%
- **`pressure_std`**: 11.68%
- **`pause_rate_per_sec`**: 11.21%
- **`normalized_jerk`**: 9.86%
- **`phonology_accuracy`**: 7.44%
- **`baseline_drift_degrees`**: 6.87%

## 4. Multimodal Fusion & Uncertainty Logic
- Late fusion weights: Structured (50%), Kinematics (30%), Handwriting (20%).
- Fallback trigger: Returns `INSUFFICIENT_EVIDENCE` when completed tasks < 40% or stroke count < 10.
- 4-Tier Evidence levels: `Elevated Concern`, `Supporting Evidence`, `Developing`, `Monitor`.
