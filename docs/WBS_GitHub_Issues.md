# 📋 Work Breakdown Structure (WBS) + GitHub Issues Plan
## AI-Based Autism and Learning Disability Screening System
**Team:** Shivam (Backend/Leader) | Supriya (Frontend) | Aarohi (ML)  
**Guide:** Prof. Sangeeta Mohapatra | AY 2026–27  

---

## 📁 GitHub Repository Setup

Create **3 repositories** on GitHub:
```
nexus-screening/
├── nexus-frontend      ← Supriya
├── nexus-backend       ← Shivam
└── nexus-ml            ← Aarohi
```

### Labels to Create in GitHub:
- 🟥 `priority: high`
- 🟨 `priority: medium`
- 🟩 `priority: low`
- 🔵 `type: feature`
- 🟠 `type: bug`
- 🔷 `type: docs`
- ✅ `status: todo`
- 🔄 `status: in-progress`
- ✔️ `status: done`

---

## 🏁 Milestones

| Milestone | Due Date | Description |
|-----------|----------|-------------|
| M1 - Setup | Week 1 | Tools, repos, environment |
| M2 - Auth | Week 4 | Login/Register working end-to-end |
| M3 - Assessment | Week 6 | Assessment UI + Data Capture |
| M4 - ML | Week 8 | ML models + Flask API live |
| M5 - Integration | Week 10 | All 3 parts connected |
| M6 - Reports | Week 11 | Reports + Clinician Review |
| M7 - Final | Week 12 | Testing + Documentation |

---

## 👑 SHIVAM — Backend Issues (nexus-backend)

### 📦 Milestone M1: Setup
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| BE-01 | Initialize Spring Boot project with Java 17 | HIGH | 2 hrs |
| BE-02 | Configure MySQL database connection | HIGH | 1 hr |
| BE-03 | Configure MongoDB connection | MEDIUM | 1 hr |
| BE-04 | Create base project folder structure | HIGH | 1 hr |
| BE-05 | Set up GitHub repo + .gitignore | HIGH | 30 min |
| BE-06 | Add Swagger/OpenAPI documentation | MEDIUM | 2 hrs |

### 📦 Milestone M2: Auth
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| BE-07 | Create User entity/model (id, name, email, password, role) | HIGH | 1 hr |
| BE-08 | Create UserRepository (JPA) | HIGH | 30 min |
| BE-09 | Implement POST /api/auth/register endpoint | HIGH | 2 hrs |
| BE-10 | Implement POST /api/auth/login endpoint | HIGH | 2 hrs |
| BE-11 | Configure JWT token generation and validation | HIGH | 3 hrs |
| BE-12 | Implement RBAC (Role-Based Access Control) | HIGH | 2 hrs |
| BE-13 | Test auth APIs with Postman | HIGH | 1 hr |

### 📦 Milestone M3: Child & Consent
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| BE-14 | Create Child entity (name, dob, grade, language, schoolType) | HIGH | 1 hr |
| BE-15 | Implement CRUD APIs for Child Profile | HIGH | 3 hrs |
| BE-16 | Create Consent entity and repository | HIGH | 1 hr |
| BE-17 | Implement POST /api/consent (store consent) | HIGH | 2 hrs |
| BE-18 | Implement GET /api/consent/check/{childId} | HIGH | 1 hr |

### 📦 Milestone M3: Assessment APIs
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| BE-19 | Create Assessment entity (child, assessor, start/end, status) | HIGH | 1 hr |
| BE-20 | Implement POST /api/assessment/start | HIGH | 2 hrs |
| BE-21 | Implement POST /api/assessment/complete | HIGH | 2 hrs |
| BE-22 | Create Task entity with age_band and type | HIGH | 2 hrs |
| BE-23 | Implement GET /api/tasks/recommend/{childId} (age-adaptive) | HIGH | 3 hrs |
| BE-24 | Implement POST /api/results (store task result) | HIGH | 2 hrs |

### 📦 Milestone M4–M5: ML Integration & Reports
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| BE-25 | Implement POST /api/analysis (call Flask ML service) | HIGH | 3 hrs |
| BE-26 | Create Report entity and repository | HIGH | 1 hr |
| BE-27 | Implement GET /api/reports/{assessmentId} | HIGH | 2 hrs |
| BE-28 | Implement PUT /api/reports/{id}/review (clinician notes) | HIGH | 2 hrs |
| BE-29 | Implement report PDF generation (JasperReports or iText) | MEDIUM | 4 hrs |
| BE-30 | Implement GET /api/children/{id}/history (longitudinal) | MEDIUM | 2 hrs |

---

## 🎨 SUPRIYA — Frontend Issues (nexus-frontend)

### 📦 Milestone M1: Setup
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-01 | Initialize React app using create-react-app | HIGH | 1 hr |
| FE-02 | Install dependencies: axios, react-router-dom, recharts | HIGH | 30 min |
| FE-03 | Set up routing structure (react-router-dom) | HIGH | 1 hr |
| FE-04 | Create global CSS variables + color palette | HIGH | 1 hr |
| FE-05 | Set up GitHub repo + .gitignore | HIGH | 30 min |

### 📦 Milestone M2: Auth UI
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-06 | Build Login page (email + password form) | HIGH | 2 hrs |
| FE-07 | Build Register page (name, email, password, role dropdown) | HIGH | 2 hrs |
| FE-08 | Connect Login to POST /api/auth/login (Axios) | HIGH | 1 hr |
| FE-09 | Store JWT token in localStorage | HIGH | 30 min |
| FE-10 | Build protected route (redirect if not logged in) | HIGH | 1 hr |

### 📦 Milestone M2: Dashboards
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-11 | Build Parent Dashboard (children list + reports) | HIGH | 3 hrs |
| FE-12 | Build Teacher Dashboard (children + assessment buttons) | HIGH | 3 hrs |
| FE-13 | Build Clinician Dashboard (pending reviews list) | HIGH | 3 hrs |
| FE-14 | Build Admin Dashboard (user management) | MEDIUM | 3 hrs |

### 📦 Milestone M3: Child Profile UI
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-15 | Build Add Child Profile form (name, DOB, grade, language) | HIGH | 2 hrs |
| FE-16 | Build Child Profile view page | HIGH | 2 hrs |
| FE-17 | Build Consent Form page (display + agree button) | HIGH | 2 hrs |
| FE-18 | Connect child CRUD to backend APIs | HIGH | 2 hrs |

### 📦 Milestone M3: Assessment UI
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-19 | Build task selection screen (adaptive task list) | HIGH | 2 hrs |
| FE-20 | Build HTML5 Canvas drawing/writing component | HIGH | 4 hrs |
| FE-21 | Capture stroke data (x, y, timestamp, pressure) from canvas | HIGH | 3 hrs |
| FE-22 | Build phonology/reading task UI (audio + response buttons) | HIGH | 3 hrs |
| FE-23 | Build task timer and progress indicator | MEDIUM | 2 hrs |

### 📦 Milestone M5–M6: Results & Reports
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| FE-24 | Build Developmental Profile display (color-coded) | HIGH | 3 hrs |
| FE-25 | Build SHAP feature importance chart (bar chart) | HIGH | 2 hrs |
| FE-26 | Build Evidence Quality indicator (completeness, uncertainty) | HIGH | 2 hrs |
| FE-27 | Build Clinician Review form (notes + sign-off button) | HIGH | 2 hrs |
| FE-28 | Build Progress Chart (line chart per modality over time) | MEDIUM | 3 hrs |
| FE-29 | Add PDF download button for reports | MEDIUM | 1 hr |

---

## 🤖 AAROHI — ML Issues (nexus-ml)

### 📦 Milestone M1: Setup
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| ML-01 | Create Python virtual environment + requirements.txt | HIGH | 1 hr |
| ML-02 | Install: pandas, numpy, scikit-learn, flask, shap, matplotlib | HIGH | 30 min |
| ML-03 | Set up Jupyter notebook environment | HIGH | 30 min |
| ML-04 | Set up GitHub repo + .gitignore | HIGH | 30 min |

### 📦 Milestone M2–M3: Data & Feature Extraction
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| ML-05 | Research and collect/generate sample dataset for training | HIGH | 5 hrs |
| ML-06 | Write stroke feature extractor (velocity, acceleration, jerk) | HIGH | 4 hrs |
| ML-07 | Write pen-lift and pause counter from stroke events | HIGH | 3 hrs |
| ML-08 | Write curvature and alignment calculator | HIGH | 3 hrs |
| ML-09 | Build feature vector: F = [accuracy, time, pressure, velocity, ...] | HIGH | 2 hrs |
| ML-10 | Write preprocessing pipeline (normalize, handle missing) | HIGH | 2 hrs |

### 📦 Milestone M4: Model Training
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| ML-11 | Train Random Forest on structured task features | HIGH | 3 hrs |
| ML-12 | Train XGBoost on structured task features | HIGH | 3 hrs |
| ML-13 | Compare RF vs XGBoost (accuracy, F1, ROC-AUC) | HIGH | 2 hrs |
| ML-14 | Train CNN on handwriting images | HIGH | 6 hrs |
| ML-15 | Implement late fusion (weighted average / meta-model) | HIGH | 4 hrs |
| ML-16 | Add SHAP explainability for top features | HIGH | 3 hrs |
| ML-17 | Add INSUFFICIENT EVIDENCE fallback (low quality data) | HIGH | 2 hrs |
| ML-18 | Save trained models as .pkl / .h5 files | HIGH | 1 hr |
| ML-19 | Evaluate model performance + write evaluation report | HIGH | 3 hrs |

### 📦 Milestone M4–M5: Flask API
| Issue # | Title | Priority | Effort |
|---------|-------|----------|--------|
| ML-20 | Create Flask app (app.py) | HIGH | 1 hr |
| ML-21 | Implement POST /predict endpoint (accepts features, returns evidence) | HIGH | 3 hrs |
| ML-22 | Load saved models at Flask startup | HIGH | 1 hr |
| ML-23 | Return response: {evidence_level, shap_values, uncertainty} | HIGH | 2 hrs |
| ML-24 | Test Flask API with Postman | HIGH | 1 hr |
| ML-25 | Add input validation + error handling in Flask | MEDIUM | 2 hrs |

---

## 🤝 SHARED TASKS (All Members)

| Issue # | Title | Assignee | Priority |
|---------|-------|---------|----------|
| SH-01 | Write project synopsis (2 pages) | All | HIGH |
| SH-02 | Create GitHub organization + repos | Shivam | HIGH |
| SH-03 | Add all members as GitHub collaborators | Shivam | HIGH |
| SH-04 | Weekly meeting notes (Google Docs) | All | MEDIUM |
| SH-05 | Create Postman collection for all APIs | Shivam + Supriya | MEDIUM |
| SH-06 | Write final project report | All | HIGH |
| SH-07 | Prepare final presentation slides | All | HIGH |
| SH-08 | Record project demo video | All | MEDIUM |

---

## 📊 Effort Summary

| Member | Total Issues | Estimated Hours |
|--------|-------------|----------------|
| Shivam (Backend) | 30 issues | ~55 hours |
| Supriya (Frontend) | 29 issues | ~55 hours |
| Aarohi (ML) | 25 issues | ~60 hours |
| Shared | 8 issues | ~15 hours |
| **TOTAL** | **92 issues** | **~185 hours** |

---

## 🔄 Git Workflow (How to Push Code)

```bash
# Every day before starting work:
git pull origin main

# After making changes:
git add .
git commit -m "feat: add login API (BE-09)"
git push origin main
```

### Commit Message Format:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation
- `test:` — adding tests

Example: `feat: implement JWT token generation (BE-11)`

---

*WBS v1.0 — AI-Based Autism and Learning Disability Screening System — ADYPSOE, SPPU, 2026–27*
