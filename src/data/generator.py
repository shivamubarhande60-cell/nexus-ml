"""
Dataset Generator for Autism Spectrum & Learning Disability Screening (ML-05).
Generates clinically grounded synthetic screening data across 4 age bands (5-12 years).
"""
import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any


def generate_synthetic_screening_dataset(
    n_samples: int = 1500,
    random_seed: int = 42
) -> pd.DataFrame:
    """
    Generates realistic multimodal screening dataset based on clinical literature:
    - Typical: High accuracy, low jerk, smooth velocity, low pause rate
    - Dyslexia Risk: Lower phonology accuracy, high rapid naming latency
    - Dysgraphia Risk: High normalized jerk, high pen lifts, high baseline drift, variable pressure
    - ASD / Motor Risk: High hesitation pauses, variable velocity, elevated jerk, fine-motor delays
    """
    np.random.seed(random_seed)

    # 55% typical developing, 45% showing mild-to-elevated screening indicators
    labels = np.random.choice([0, 1], size=n_samples, p=[0.55, 0.45])
    
    # Subtype distribution among positive indicators
    subtypes = []
    for lbl in labels:
        if lbl == 0:
            subtypes.append("Typical")
        else:
            subtypes.append(np.random.choice([
                "Dyslexia_Risk",
                "Dysgraphia_Risk",
                "ASD_Motor_Risk",
                "Mixed_Risk"
            ], p=[0.35, 0.30, 0.20, 0.15]))

    # Age: 5 to 12 uniformly sampled
    age = np.random.uniform(5.0, 12.0, size=n_samples)
    grade = np.clip(np.round(age - 5.0), 1, 6)

    # Base structured indicators (age-scaled)
    phonology_acc = np.zeros(n_samples)
    phonology_latency = np.zeros(n_samples)
    rapid_naming_speed = np.zeros(n_samples)
    reading_accuracy = np.zeros(n_samples)
    working_memory = np.zeros(n_samples)

    # Kinematics & Handwriting indicators
    mean_velocity = np.zeros(n_samples)
    normalized_jerk = np.zeros(n_samples)
    pen_lift_count = np.zeros(n_samples)
    in_air_ratio = np.zeros(n_samples)
    pause_rate = np.zeros(n_samples)
    mean_pressure = np.zeros(n_samples)
    pressure_std = np.zeros(n_samples)
    tortuosity = np.zeros(n_samples)
    baseline_drift = np.zeros(n_samples)

    for i in range(n_samples):
        st = subtypes[i]
        curr_age = age[i]
        age_factor = (curr_age - 5.0) / 7.0  # Normalized maturity progress [0, 1]

        if st == "Typical":
            phonology_acc[i] = np.clip(np.random.normal(0.85 + 0.10 * age_factor, 0.06), 0.65, 1.0)
            phonology_latency[i] = np.clip(np.random.normal(1200 - 300 * age_factor, 150), 600, 2200)
            rapid_naming_speed[i] = np.clip(np.random.normal(2.5 + 1.0 * age_factor, 0.4), 1.2, 5.0)
            reading_accuracy[i] = np.clip(np.random.normal(0.88 + 0.08 * age_factor, 0.05), 0.70, 1.0)
            working_memory[i] = np.clip(np.random.normal(0.82 + 0.12 * age_factor, 0.08), 0.60, 1.0)

            mean_velocity[i] = np.clip(np.random.normal(120 + 40 * age_factor, 20), 70, 220)
            normalized_jerk[i] = np.clip(np.random.normal(25 - 8 * age_factor, 6), 8, 45)
            pen_lift_count[i] = np.random.poisson(max(3, int(6 - 2 * age_factor)))
            in_air_ratio[i] = np.clip(np.random.normal(0.18, 0.04), 0.05, 0.32)
            pause_rate[i] = np.clip(np.random.normal(0.25, 0.08), 0.05, 0.50)
            mean_pressure[i] = np.clip(np.random.normal(0.55, 0.08), 0.35, 0.75)
            pressure_std[i] = np.clip(np.random.normal(0.08, 0.02), 0.03, 0.16)
            tortuosity[i] = np.clip(np.random.normal(1.15, 0.08), 1.02, 1.40)
            baseline_drift[i] = np.clip(np.random.normal(2.5, 1.2), 0.2, 6.0)

        elif st == "Dyslexia_Risk":
            phonology_acc[i] = np.clip(np.random.normal(0.52 + 0.08 * age_factor, 0.09), 0.25, 0.72)
            phonology_latency[i] = np.clip(np.random.normal(2400 - 300 * age_factor, 350), 1400, 4200)
            rapid_naming_speed[i] = np.clip(np.random.normal(1.3 + 0.4 * age_factor, 0.3), 0.6, 2.3)
            reading_accuracy[i] = np.clip(np.random.normal(0.50 + 0.10 * age_factor, 0.10), 0.20, 0.72)
            working_memory[i] = np.clip(np.random.normal(0.60 + 0.10 * age_factor, 0.10), 0.35, 0.80)

            # Motor kinematics mostly normal
            mean_velocity[i] = np.clip(np.random.normal(110 + 35 * age_factor, 22), 65, 200)
            normalized_jerk[i] = np.clip(np.random.normal(30 - 6 * age_factor, 8), 12, 55)
            pen_lift_count[i] = np.random.poisson(max(4, int(7 - 2 * age_factor)))
            in_air_ratio[i] = np.clip(np.random.normal(0.22, 0.06), 0.08, 0.40)
            pause_rate[i] = np.clip(np.random.normal(0.35, 0.10), 0.10, 0.70)
            mean_pressure[i] = np.clip(np.random.normal(0.54, 0.09), 0.30, 0.80)
            pressure_std[i] = np.clip(np.random.normal(0.10, 0.03), 0.04, 0.20)
            tortuosity[i] = np.clip(np.random.normal(1.22, 0.10), 1.05, 1.60)
            baseline_drift[i] = np.clip(np.random.normal(3.8, 1.8), 0.5, 9.0)

        elif st == "Dysgraphia_Risk":
            # Cognitive phonology normal, motor/stroke heavily impaired
            phonology_acc[i] = np.clip(np.random.normal(0.80 + 0.10 * age_factor, 0.08), 0.60, 0.98)
            phonology_latency[i] = np.clip(np.random.normal(1400 - 250 * age_factor, 200), 800, 2400)
            rapid_naming_speed[i] = np.clip(np.random.normal(2.2 + 0.8 * age_factor, 0.4), 1.0, 4.2)
            reading_accuracy[i] = np.clip(np.random.normal(0.82 + 0.08 * age_factor, 0.08), 0.62, 0.98)
            working_memory[i] = np.clip(np.random.normal(0.75 + 0.10 * age_factor, 0.09), 0.50, 0.95)

            mean_velocity[i] = np.clip(np.random.normal(75 + 20 * age_factor, 18), 35, 130)
            normalized_jerk[i] = np.clip(np.random.normal(72 - 12 * age_factor, 15), 38, 140)
            pen_lift_count[i] = np.random.poisson(int(14 - 3 * age_factor))
            in_air_ratio[i] = np.clip(np.random.normal(0.38, 0.08), 0.20, 0.65)
            pause_rate[i] = np.clip(np.random.normal(0.68, 0.15), 0.30, 1.25)
            mean_pressure[i] = np.clip(np.random.normal(0.78, 0.12), 0.45, 0.98)
            pressure_std[i] = np.clip(np.random.normal(0.24, 0.06), 0.12, 0.45)
            tortuosity[i] = np.clip(np.random.normal(1.65, 0.22), 1.25, 2.50)
            baseline_drift[i] = np.clip(np.random.normal(9.5, 3.2), 3.0, 22.0)

        elif st == "ASD_Motor_Risk":
            # Multi-domain motor planning and attentional variability
            phonology_acc[i] = np.clip(np.random.normal(0.68 + 0.08 * age_factor, 0.12), 0.40, 0.90)
            phonology_latency[i] = np.clip(np.random.normal(2100 - 300 * age_factor, 400), 1200, 3800)
            rapid_naming_speed[i] = np.clip(np.random.normal(1.6 + 0.6 * age_factor, 0.4), 0.8, 3.2)
            reading_accuracy[i] = np.clip(np.random.normal(0.72 + 0.08 * age_factor, 0.10), 0.45, 0.92)
            working_memory[i] = np.clip(np.random.normal(0.58 + 0.10 * age_factor, 0.12), 0.30, 0.85)

            mean_velocity[i] = np.clip(np.random.normal(82 + 25 * age_factor, 20), 40, 145)
            normalized_jerk[i] = np.clip(np.random.normal(64 - 10 * age_factor, 14), 32, 120)
            pen_lift_count[i] = np.random.poisson(int(11 - 2 * age_factor))
            in_air_ratio[i] = np.clip(np.random.normal(0.34, 0.07), 0.16, 0.55)
            pause_rate[i] = np.clip(np.random.normal(0.75, 0.18), 0.32, 1.40)
            mean_pressure[i] = np.clip(np.random.normal(0.42, 0.14), 0.18, 0.85)
            pressure_std[i] = np.clip(np.random.normal(0.20, 0.05), 0.09, 0.38)
            tortuosity[i] = np.clip(np.random.normal(1.52, 0.20), 1.15, 2.20)
            baseline_drift[i] = np.clip(np.random.normal(7.8, 2.8), 2.0, 18.0)

        else:  # Mixed Risk
            phonology_acc[i] = np.clip(np.random.normal(0.54, 0.10), 0.28, 0.75)
            phonology_latency[i] = np.clip(np.random.normal(2500, 380), 1500, 4100)
            rapid_naming_speed[i] = np.clip(np.random.normal(1.3, 0.3), 0.5, 2.2)
            reading_accuracy[i] = np.clip(np.random.normal(0.55, 0.11), 0.25, 0.78)
            working_memory[i] = np.clip(np.random.normal(0.52, 0.10), 0.28, 0.75)

            mean_velocity[i] = np.clip(np.random.normal(70, 18), 35, 120)
            normalized_jerk[i] = np.clip(np.random.normal(75, 16), 40, 140)
            pen_lift_count[i] = np.random.poisson(13)
            in_air_ratio[i] = np.clip(np.random.normal(0.40, 0.08), 0.22, 0.65)
            pause_rate[i] = np.clip(np.random.normal(0.80, 0.18), 0.35, 1.50)
            mean_pressure[i] = np.clip(np.random.normal(0.72, 0.14), 0.35, 0.98)
            pressure_std[i] = np.clip(np.random.normal(0.22, 0.06), 0.10, 0.42)
            tortuosity[i] = np.clip(np.random.normal(1.60, 0.22), 1.20, 2.40)
            baseline_drift[i] = np.clip(np.random.normal(9.0, 3.0), 3.0, 20.0)

    df = pd.DataFrame({
        "age_years": np.round(age, 1),
        "grade": grade.astype(int),
        "phonology_accuracy": np.round(phonology_acc, 3),
        "phonology_latency_ms": np.round(phonology_latency, 1),
        "rapid_naming_speed": np.round(rapid_naming_speed, 2),
        "reading_accuracy": np.round(reading_accuracy, 3),
        "working_memory_score": np.round(working_memory, 3),
        "mean_velocity": np.round(mean_velocity, 2),
        "normalized_jerk": np.round(normalized_jerk, 2),
        "pen_lift_count": pen_lift_count.astype(int),
        "in_air_ratio": np.round(in_air_ratio, 3),
        "pause_rate_per_sec": np.round(pause_rate, 3),
        "mean_pressure": np.round(mean_pressure, 3),
        "pressure_std": np.round(pressure_std, 3),
        "tortuosity": np.round(tortuosity, 3),
        "baseline_drift_degrees": np.round(baseline_drift, 2),
        "subtype": subtypes,
        "screening_label": labels
    })
    return df
