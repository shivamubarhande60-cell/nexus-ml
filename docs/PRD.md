# 📄 Product Requirements Document (PRD)
## AI-Based Autism and Learning Disability Screening System
**Version:** 1.0  
**Date:** October 2026  
**Institution:** Ajeenkya DY Patil School of Engineering, SPPU  
**Department:** Computer Engineering  
**Guide:** Prof. Sangeeta Mohapatra  
**Team:** Shivam Ubarhande (Leader) | Supriya Unde | Aarohi Wagh  

---

## 1. 🎯 Product Overview

### 1.1 What Is This Product?
A full-stack AI/ML-powered **screening support platform** that evaluates children's learning, handwriting, drawing, and behavioural evidence to generate **transparent developmental indicators** for:
- **Autism Spectrum Disorder (ASD)**
- **Learning Disabilities (LD)** — Dyslexia, Dyscalculia, Dysgraphia

> ⚠️ **Critical Disclaimer:** This system provides **screening support only — NOT a diagnosis.** All results must be reviewed by a licensed professional (doctor/psychologist).

### 1.2 One-Line Summary
> *"Organize meaningful evidence about a child's development to support earlier and more informed professional next steps."*

---

## 2. 👥 Who Will Use This? (User Personas)

| User | Role | What They Do in the System |
|------|------|---------------------------|
| **Parent** | Initiates screening | Registers child, gives consent, fills context questionnaire |
| **Teacher / Special Educator** | Conducts assessment | Runs digital tasks with the child, monitors progress |
| **Clinician / Psychologist** | Reviews results | Views developmental profile, writes professional review |
| **Admin** | Manages platform | Manages user accounts, roles, and system settings |

---

## 3. 🚩 Problem Statement

Current challenges in early ASD/LD screening:

1. **Single-signal reliance** — one questionnaire or test is not enough
2. **Fixed assessments** — same task for all ages is unfair & inaccurate
3. **Black-box AI** — no explanation for why a result was generated
4. **No longitudinal tracking** — can't compare child's progress over time
5. **Accessibility** — expensive, clinic-only assessments are not reachable for all

---

## 4. 🎯 Goals & Objectives

| # | Goal | Success Criteria |
|---|------|-----------------|
| G1 | Age-appropriate adaptive assessment | Tasks auto-selected based on age (5–12 yrs) |
| G2 | Multimodal evidence collection | At least 5 modalities captured per session |
| G3 | AI-generated developmental profile | Profile generated within 30 seconds of task completion |
| G4 | Explainable results | Top contributing features shown for every result |
| G5 | Professional review loop | Clinician can annotate, override and sign off on every report |
| G6 | Longitudinal tracking | Progress comparison across multiple sessions |
| G7 | Secure role-based access | Each user sees only what they are allowed to see |

---

## 5. ✅ Functional Requirements (What the System Must Do)

### 5.1 Authentication & User Management
- [ ] FR-01: User can register with name, email, password, and role
- [ ] FR-02: User can log in and receive a secure JWT token
- [ ] FR-03: Roles: Parent, Teacher, Clinician, Admin (each sees different screens)
- [ ] FR-04: Admin can create/deactivate user accounts

### 5.2 Child Profile Management
- [ ] FR-05: Parent/Teacher can create a child profile (name, DOB, grade, language, school type)
- [ ] FR-06: System auto-calculates child's age from DOB
- [ ] FR-07: Multiple children can be linked to one parent/teacher account
- [ ] FR-08: Profile stores educational exposure and prior assessment history

### 5.3 Consent Management
- [ ] FR-09: Parent must give digital consent before any assessment
- [ ] FR-10: Consent records are stored with timestamp and user ID
- [ ] FR-11: No data is collected without valid consent on file

### 5.4 Adaptive Assessment Engine
- [ ] FR-12: System selects age-appropriate tasks automatically
  - Age 5–7: Pre-literacy, phonology, tracing
  - Age 6–8: Letter-sound mapping, early decoding
  - Age 8–10: Word recognition, fluency, comprehension
  - Age 10–12: Advanced reading, written expression
- [ ] FR-13: If child struggles, system steps down to simpler prerequisite task
- [ ] FR-14: Teacher can manually override task selection
- [ ] FR-15: Assessment sessions can be paused and resumed

### 5.5 Data Capture
- [ ] FR-16: Capture on-screen drawing/writing input (x, y coordinates, timestamps, pressure, pen state)
- [ ] FR-17: Capture task response accuracy and latency
- [ ] FR-18: Capture audio responses (optional, with consent)
- [ ] FR-19: Optional: capture webcam facial landmarks (experimental, consent required)

### 5.6 Feature Extraction & AI Analysis
- [ ] FR-20: Extract stroke kinematics: velocity, acceleration, jerk, curvature, pauses, pen lifts
- [ ] FR-21: Extract learning features: accuracy, phonology latency, spelling errors
- [ ] FR-22: Run specialized ML model per modality (Structured, Handwriting, Kinematics)
- [ ] FR-23: Combine evidence using late fusion model
- [ ] FR-24: Return evidence level: Elevated Concern / Supporting Evidence / Developing / Monitor
- [ ] FR-25: Return SHAP-based explanation (top features contributing to result)
- [ ] FR-26: Return uncertainty indicator (data quality, evidence agreement)

### 5.7 Report & Professional Review
- [ ] FR-27: Auto-generate developmental profile report after session
- [ ] FR-28: Clinician can view full report, add notes, and sign off
- [ ] FR-29: Report includes: profile, evidence quality, explanation, recommended next step
- [ ] FR-30: Completed report is downloadable as PDF

### 5.8 Longitudinal Tracking
- [ ] FR-31: Dashboard shows assessment history for each child
- [ ] FR-32: Progress charts compare scores across sessions
- [ ] FR-33: System flags if a child's indicators worsen over time

---

## 6. 🚫 Out of Scope (What We Are NOT Building)

| Item | Reason |
|------|--------|
| Medical diagnosis | This is a screening tool only |
| Real-time video analysis | Too complex for current scope |
| Full EHR/EMR integration | Not required for BE project |
| Mobile app (Android/iOS) | Web-only for this version |
| Speech-to-text engine | Out of timeline scope |
| Billing / payment system | Not applicable |

---

## 7. 🛠️ Technical Requirements (Non-Functional)

| Category | Requirement |
|----------|-------------|
| **Performance** | API response time < 2 seconds for non-ML endpoints |
| **ML Inference** | Prediction result returned within 30 seconds |
| **Security** | JWT authentication + RBAC for all routes |
| **Data Privacy** | No raw child images/videos stored without explicit consent |
| **Availability** | System works on Chrome/Edge/Firefox browsers |
| **Database** | MySQL for structured data, MongoDB for stroke event streams |
| **Scalability** | Minimum 100 concurrent users supported |

---

## 8. 📐 System Architecture (High Level)

```
┌─────────────────────────────────────────────────────────────┐
│                  USER (Browser)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────────┐
│           FRONTEND  (React + Tailwind CSS)                   │
│   Login | Dashboard | Assessment UI | Report Viewer          │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API (JSON)
┌──────────────────────▼──────────────────────────────────────┐
│         BACKEND  (Java 17 + Spring Boot)                     │
│   Auth | Child Mgmt | Session | Report | Review API          │
└──────────┬────────────────────────────┬─────────────────────┘
           │ SQL                        │ HTTP
┌──────────▼──────────┐   ┌────────────▼─────────────────────┐
│  MySQL + MongoDB    │   │    AI/ML Service (Python+Flask)   │
│  Users, Sessions,   │   │   Feature Extraction + Models +   │
│  Reports, Consent   │   │   SHAP Explainability             │
└─────────────────────┘   └──────────────────────────────────┘
```

---

## 9. 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Assessment completion rate | > 80% of started sessions completed |
| Clinician review rate | 100% of reports reviewed before finalising |
| False positive rate | Tracked and minimised (clinician feedback loop) |
| System uptime | > 95% during academic year |
| User satisfaction (teachers/parents) | > 4/5 average rating |

---

## 10. 📅 Milestone Plan

| Milestone | Deliverable | Target |
|-----------|-------------|--------|
| M1 | Tools installed + GitHub repos created | Week 1 |
| M2 | Login + Child Profile working (Backend + Frontend) | Week 4 |
| M3 | Assessment UI + Data Capture working | Week 6 |
| M4 | ML model trained + Flask API live | Week 8 |
| M5 | Full integration (all 3 parts connected) | Week 10 |
| M6 | Report generation + Clinician review working | Week 11 |
| M7 | Final testing + Bug fixes + Documentation | Week 12 |

---

*Document prepared for BE Final Year Project, AY 2026–27*
