# 🤖 Nexus AI/ML (Screening Intelligence Service)
**Lead Developer:** Aarohi Wagh  
**Technologies:** Python 3.12, Scikit-learn, XGBoost, TensorFlow/Keras, Flask/FastAPI, SHAP

---

## 📌 Your Roadmap from the PRD
1. **Kinematics Feature Extraction**: Compute velocity, acceleration, jerk, pauses, pen-lifts from stroke coordinate streams.
2. **Model 1 (Structured Data)**: Random Forest / XGBoost models for phonology, reading accuracy, and response latency.
3. **Model 2 (Handwriting Analysis)**: CNN / image classifier for handwritten shapes and letter tracing.
4. **Multimodal Late Fusion**: Combine independent modality outputs with uncertainty estimation into a unified profile.
5. **Explainability**: SHAP value calculation for top contributing features.
6. **Inference Service**: A lightweight REST API (POST /predict) callable by the Spring Boot backend.

All official project specifications are located in the [docs/](./docs) folder:
- [PRD.md](./docs/PRD.md)
- [SRS.md](./docs/SRS.md)
- [Task Breakdown (WBS)](./docs/WBS_GitHub_Issues.md)
