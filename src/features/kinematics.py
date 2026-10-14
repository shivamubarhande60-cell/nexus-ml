"""
Kinematics Feature Extractor for Stroke Coordinate Streams (ML-06).
Computes velocity, acceleration, jerk, and motion smoothness metrics.
"""
from typing import List, Dict, Any
import numpy as np


def extract_kinematic_features(stroke_points: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Extracts dynamic kinematic features from raw stroke coordinate sequence.
    
    Each point is expected to have:
      - 'x': float (horizontal pixel/mm coordinate)
      - 'y': float (vertical pixel/mm coordinate)
      - 't': float (timestamp in milliseconds)
      - 'pressure': float [0.0, 1.0] (stylus/touch pressure)
    """
    default_kinematics = {
        "mean_velocity": 0.0,
        "peak_velocity": 0.0,
        "velocity_std": 0.0,
        "mean_acceleration": 0.0,
        "peak_acceleration": 0.0,
        "mean_jerk": 0.0,
        "normalized_jerk": 0.0,
        "total_path_length": 0.0,
        "stroke_duration_ms": 0.0
    }

    if not stroke_points or len(stroke_points) < 4:
        return default_kinematics

    # Extract coordinates into numpy arrays
    x = np.array([p.get("x", 0.0) for p in stroke_points], dtype=float)
    y = np.array([p.get("y", 0.0) for p in stroke_points], dtype=float)
    t = np.array([p.get("t", 0.0) for p in stroke_points], dtype=float)

    # Convert timestamps from ms to seconds for standard physical units
    t_sec = (t - t[0]) / 1000.0

    # Handle duplicate or non-increasing timestamps safely
    dt = np.diff(t_sec)
    dt[dt <= 0.0001] = 0.001  # Minimum 1ms spacing to prevent division by zero

    # Distances between consecutive points
    dx = np.diff(x)
    dy = np.diff(y)
    distances = np.sqrt(dx**2 + dy**2)
    total_length = float(np.sum(distances))
    total_duration = float(t[-1] - t[0])

    # First derivative: Instantaneous Velocity (px/sec)
    velocities = distances / dt
    mean_vel = float(np.mean(velocities))
    peak_vel = float(np.max(velocities))
    std_vel = float(np.std(velocities))

    # Second derivative: Instantaneous Acceleration (px/sec^2)
    dt_mid = (dt[:-1] + dt[1:]) / 2.0
    dt_mid[dt_mid <= 0.0001] = 0.001
    dv = np.diff(velocities)
    accelerations = np.abs(dv / dt_mid)
    mean_acc = float(np.mean(accelerations)) if len(accelerations) > 0 else 0.0
    peak_acc = float(np.max(accelerations)) if len(accelerations) > 0 else 0.0

    # Third derivative: Jerk (Rate of change of acceleration - px/sec^3)
    # Jerk is an established clinical biomarker for motor control & dysgraphia
    if len(accelerations) > 1:
        dt_jerk = (dt_mid[:-1] + dt_mid[1:]) / 2.0
        dt_jerk[dt_jerk <= 0.0001] = 0.001
        da = np.diff(accelerations)
        jerk_values = np.abs(da / dt_jerk)
        mean_jerk = float(np.mean(jerk_values))
        
        # Dimensionless Normalized Jerk (smoothness metric independent of size/speed)
        # NJ = sqrt(0.5 * integral(jerk^2) * duration^5 / length^2)
        duration_s = max(total_duration / 1000.0, 0.01)
        dt_step = float(np.mean(dt_jerk))
        if hasattr(np, "trapezoid"):
            jerk_integral = float(np.trapezoid(jerk_values**2, dx=dt_step))
        elif hasattr(np, "trapz"):
            jerk_integral = float(np.trapz(jerk_values**2, dx=dt_step))
        else:
            jerk_integral = float(np.sum(jerk_values**2) * dt_step)
        length_safe = max(total_length, 1.0)
        normalized_jerk = float(np.sqrt(0.5 * jerk_integral * (duration_s**5) / (length_safe**2)))
    else:
        mean_jerk = 0.0
        normalized_jerk = 0.0

    return {
        "mean_velocity": round(mean_vel, 4),
        "peak_velocity": round(peak_vel, 4),
        "velocity_std": round(std_vel, 4),
        "mean_acceleration": round(mean_acc, 4),
        "peak_acceleration": round(peak_acc, 4),
        "mean_jerk": round(mean_jerk, 4),
        "normalized_jerk": round(min(normalized_jerk, 1000.0), 4),
        "total_path_length": round(total_length, 4),
        "stroke_duration_ms": round(total_duration, 2)
    }
