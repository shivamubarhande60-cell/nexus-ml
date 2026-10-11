# 📄 Software Requirements Specification (SRS)
## AI-Based Autism and Learning Disability Screening System
**Document Version:** 1.0  
**Date:** October 2026  
**Standard:** Based on IEEE 830 SRS Format  
**Institution:** Ajeenkya DY Patil School of Engineering (SPPU)  
**Department:** Computer Engineering  

---

## 1. INTRODUCTION

### 1.1 Purpose
This SRS document describes the software requirements for an AI/ML-based multimodal screening support system for children (ages 5–12) who may show indicators of Autism Spectrum Disorder (ASD) or Learning Disabilities (LD). It is intended for the development team, guide, and evaluators.

### 1.2 Scope
The system is named **NexusScreen** (working title). It is a web-based platform that:
- Collects multimodal evidence from digital assessment tasks
- Processes evidence using specialized ML models
- Produces an explainable developmental profile
- Supports professional clinician review and longitudinal tracking

### 1.3 Definitions

| Term | Meaning |
|------|---------|
| ASD | Autism Spectrum Disorder |
| LD | Learning Disability (Dyslexia, Dyscalculia, Dysgraphia) |
| JWT | JSON Web Token — used for secure login |
| RBAC | Role-Based Access Control |
| SHAP | SHapley Additive exPlanations — AI explainability method |
| Stroke | One pen movement on screen (from pen-down to pen-up) |
| Modality | One category of evidence (e.g., handwriting, reading) |
| Fusion | Combining evidence from multiple modalities |
| Screening | Early identification support — NOT a clinical diagnosis |

### 1.4 References
- PPT: "AI-Based Autism and Learning Disability Screening System" (Team, Oct 2026)
- CDC Clinical Testing and Diagnosis for ASD (2025)
- IDA Testing and Evaluation Guidelines
- NIMHANS SLD Framework (India)

---

## 2. OVERALL DESCRIPTION

### 2.1 Product Perspective
NexusScreen is a standalone web application. It does not integrate with hospital EMR/EHR systems in this version. It connects three internal services:
- React Frontend
- Spring Boot Backend
- Python Flask ML Service

### 2.2 Product Functions (Summary)
1. User registration & login with role-based access
2. Child profile creation with context (age, grade, language)
3. Digital consent management
4. Adaptive task selection based on child's profile
5. Interactive assessment with digital canvas
6. Automated feature extraction from responses
7. ML-based evidence generation with SHAP explanations
8. Developmental profile report generation
9. Clinician review and sign-off
10. Longitudinal progress tracking

### 2.3 User Classes

| Class | Technical Level | Frequency of Use |
|-------|----------------|-----------------|
| Parent | Low | Occasional (consent + viewing reports) |
| Teacher / Special Educator | Medium | Regular (running assessments) |
| Clinician / Psychologist | High | Regular (reviewing reports) |
| System Admin | High | As needed |

### 2.4 Operating Environment
- **Client:** Chrome, Firefox, or Edge browser (desktop/tablet)
- **Backend Server:** Java 17, Spring Boot 3.x
- **ML Server:** Python 3.11, Flask
- **Database:** MySQL 8.x + MongoDB 6.x
- **OS:** Windows / Linux (server-side)

### 2.5 Constraints
- System is NOT for clinical diagnosis
- Raw media (video/audio) not stored without consent
- System must comply with data privacy norms (India IT Act / DPDP)
- ML models must be retrained on labeled data before production use

---

## 3. SYSTEM FEATURES & REQUIREMENTS

---

### Feature 1: User Authentication

**Description:** Secure login and registration for all user types.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-1.1 | System shall allow users to register with: name, email, password, role | HIGH |
| SRS-1.2 | System shall validate email format and enforce password strength (min 8 chars) | HIGH |
| SRS-1.3 | System shall authenticate users via JWT token (expires in 24 hours) | HIGH |
| SRS-1.4 | System shall enforce role-based access (Parent ≠ Clinician ≠ Admin views) | HIGH |
| SRS-1.5 | System shall lock account after 5 failed login attempts | MEDIUM |
| SRS-1.6 | System shall allow password reset via email OTP | MEDIUM |

---

### Feature 2: Child Profile Management

**Description:** Creating and managing profiles for children to be assessed.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-2.1 | System shall allow creation of child profile with: full name, DOB, gender, grade, primary language, school type | HIGH |
| SRS-2.2 | System shall auto-calculate age from DOB at time of assessment | HIGH |
| SRS-2.3 | System shall allow linking multiple children to one parent/teacher account | HIGH |
| SRS-2.4 | System shall store educational exposure details (schooled/homeschooled, years in school) | MEDIUM |
| SRS-2.5 | System shall maintain assessment history per child | HIGH |

---

### Feature 3: Consent Management

**Description:** Ensuring legal and ethical data collection consent.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-3.1 | System shall display full consent form before any assessment begins | HIGH |
| SRS-3.2 | Parent/Guardian must digitally sign/agree before data collection | HIGH |
| SRS-3.3 | Consent record shall be stored with: user ID, child ID, timestamp, consent text version | HIGH |
| SRS-3.4 | Assessment cannot start if valid consent does not exist | HIGH |
| SRS-3.5 | Consent for experimental facial analysis must be separate | HIGH |

---

### Feature 4: Adaptive Assessment Engine

**Description:** Selecting and administering the right tasks for each child.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-4.1 | System shall select tasks based on child's age and grade | HIGH |
| SRS-4.2 | Task sets shall be defined for 4 age bands: 5–7, 6–8, 8–10, 10–12 | HIGH |
| SRS-4.3 | System shall step down to simpler tasks if child scores below threshold | HIGH |
| SRS-4.4 | Assessment shall cover at minimum: pre-literacy, writing, handwriting domains | HIGH |
| SRS-4.5 | Teacher shall be able to manually select/skip tasks | MEDIUM |
| SRS-4.6 | System shall allow pausing and resuming a session | MEDIUM |
| SRS-4.7 | Each task shall display clear, age-appropriate instructions | HIGH |

---

### Feature 5: Data Capture

**Description:** Collecting raw input from the child during assessment.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-5.1 | System shall capture stylus/mouse stroke data: x, y, pressure, timestamp, pen state | HIGH |
| SRS-5.2 | System shall capture task response: correct/incorrect, response time | HIGH |
| SRS-5.3 | Stroke data shall be stored in MongoDB as event streams | HIGH |
| SRS-5.4 | Captured image of drawing/writing shall be stored in Object Storage | MEDIUM |
| SRS-5.5 | No facial video shall be captured without separate consent (SRS-3.5) | HIGH |

---

### Feature 6: AI/ML Analysis

**Description:** Processing captured data to generate evidence.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-6.1 | System shall extract stroke kinematics: velocity, acceleration, jerk, curvature, pauses, pen lifts | HIGH |
| SRS-6.2 | System shall run Random Forest / XGBoost on structured task features | HIGH |
| SRS-6.3 | System shall run CNN on handwriting image | HIGH |
| SRS-6.4 | System shall combine modality results using late fusion | HIGH |
| SRS-6.5 | System shall return SHAP values for top contributing features | HIGH |
| SRS-6.6 | System shall return uncertainty level (INSUFFICIENT EVIDENCE if data quality is poor) | HIGH |
| SRS-6.7 | ML results shall be returned via Flask REST API | HIGH |
| SRS-6.8 | Evidence levels shall be: Elevated Concern / Supporting Evidence / Developing / Monitor | HIGH |

---

### Feature 7: Report Generation

**Description:** Producing a readable developmental profile report.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-7.1 | System shall auto-generate report after session completion | HIGH |
| SRS-7.2 | Report shall include: developmental profile, evidence quality, SHAP explanation, recommended next step | HIGH |
| SRS-7.3 | Report shall be viewable in browser and downloadable as PDF | HIGH |
| SRS-7.4 | Report shall clearly state: "Screening support only — not a diagnosis" | HIGH |

---

### Feature 8: Professional Review

**Description:** Clinician review and sign-off on generated reports.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-8.1 | Clinician shall be able to view full developmental report | HIGH |
| SRS-8.2 | Clinician can add professional notes/comments to report | HIGH |
| SRS-8.3 | Clinician can override or flag any AI-generated evidence level | HIGH |
| SRS-8.4 | Report status: Draft → Under Review → Finalised | HIGH |
| SRS-8.5 | Only finalised reports are visible to parents | HIGH |

---

### Feature 9: Longitudinal Tracking

**Description:** Tracking child's progress across multiple sessions.

| Req ID | Requirement | Priority |
|--------|-------------|----------|
| SRS-9.1 | System shall store all assessment results per child with date | HIGH |
| SRS-9.2 | Dashboard shall show progress charts per modality over time | MEDIUM |
| SRS-9.3 | System shall highlight worsening indicators | MEDIUM |

---

## 4. EXTERNAL INTERFACE REQUIREMENTS

### 4.1 User Interface
- Web-based, responsive (desktop + tablet)
- Assessment canvas must support touch and stylus input
- Color-coded developmental profile (Red = Elevated, Yellow = Monitor, Green = Developing)

### 4.2 Hardware Interface
- Stylus/tablet recommended for handwriting tasks
- Webcam optional (experimental facial analysis, consent required)

### 4.3 Software Interface
- Frontend ↔ Backend: REST API (JSON over HTTPS)
- Backend ↔ ML Service: REST API (JSON over HTTP, internal)
- Backend ↔ MySQL: JDBC / Spring Data JPA
- Backend ↔ MongoDB: Spring Data MongoDB

### 4.4 Communication Interface
- HTTPS for all external communication
- JWT Bearer Token in Authorization header

---

## 5. NON-FUNCTIONAL REQUIREMENTS

| Category | Requirement |
|----------|-------------|
| **Performance** | API response ≤ 2 sec; ML inference ≤ 30 sec |
| **Security** | JWT auth; RBAC; no raw media without consent |
| **Reliability** | 95% uptime; graceful error handling |
| **Usability** | Teacher can run full assessment without training manual |
| **Maintainability** | Code documented; modules independently deployable |
| **Privacy** | No child PII exposed in API logs |

---

## 6. APPENDIX — Database Tables (Summary)

### MySQL Tables
| Table | Key Columns |
|-------|-------------|
| `users` | id, name, email, password_hash, role, created_at |
| `children` | id, parent_id, name, dob, grade, language, school_type |
| `consents` | id, child_id, user_id, timestamp, version, signed |
| `assessments` | id, child_id, assessor_id, start_time, end_time, status |
| `tasks` | id, name, type, age_band, difficulty_level |
| `results` | id, assessment_id, task_id, accuracy, latency, evidence_level |
| `reports` | id, assessment_id, profile_json, status, clinician_id |
| `reviews` | id, report_id, clinician_id, notes, timestamp |

### MongoDB Collections
| Collection | Contents |
|------------|---------|
| `stroke_sessions` | Raw x, y, pressure, timestamp, pen_state events per task |
| `telemetry` | Page load times, errors, session events |

---

*SRS v1.0 — AI-Based Autism and Learning Disability Screening System — ADYPSOE, SPPU, 2026–27*
