"""
Stroke Events & Pen Dynamics Feature Extractor (ML-07).
Extracts pen-lifts, in-air time, pause count/duration, and stylus pressure statistics.
"""
from typing import List, Dict, Any
import numpy as np


def extract_stroke_event_features(
    stroke_points: List[Dict[str, Any]],
    pause_speed_threshold_px_s: float = 15.0,
    min_pause_duration_ms: float = 200.0
) -> Dict[str, float]:
    """
    Computes pen-lift frequency, pause metrics, and stylus pressure statistics.
    
    Parameters:
      - stroke_points: list of points with 'x', 'y', 't', 'pressure', 'pen_state' (0=up, 1=down)
      - pause_speed_threshold_px_s: speed below which movement is classified as hesitation/pause
      - min_pause_duration_ms: minimum duration in milliseconds to qualify as a clinical pause
    """
    default_events = {
        "pen_lift_count": 0,
        "on_paper_time_ms": 0.0,
        "in_air_time_ms": 0.0,
        "in_air_ratio": 0.0,
        "pause_count": 0,
        "total_pause_duration_ms": 0.0,
        "pause_rate_per_sec": 0.0,
        "mean_pressure": 0.0,
        "pressure_std": 0.0,
        "abrupt_pressure_changes": 0
    }

    if not stroke_points or len(stroke_points) < 4:
        return default_events

    x = np.array([p.get("x", 0.0) for p in stroke_points], dtype=float)
    y = np.array([p.get("y", 0.0) for p in stroke_points], dtype=float)
    t = np.array([p.get("t", 0.0) for p in stroke_points], dtype=float)
    pressure = np.array([p.get("pressure", 0.5) for p in stroke_points], dtype=float)
    # pen_state: 1 for touching surface (down), 0 for hovering/in-air (up)
    pen_state = np.array([p.get("pen_state", 1 if p.get("pressure", 0.5) > 0.05 else 0) for p in stroke_points], dtype=int)

    # 1. Pen-Lift Analysis
    # Transitions from 1 (down) to 0 (up) indicate a pen lift
    state_transitions = np.diff(pen_state)
    pen_lifts = int(np.sum(state_transitions == -1))

    dt = np.diff(t)
    dt[dt <= 0] = 1.0  # safe interval

    on_paper_time = float(np.sum(dt[pen_state[:-1] == 1])) if len(dt) > 0 else 0.0
    in_air_time = float(np.sum(dt[pen_state[:-1] == 0])) if len(dt) > 0 else 0.0
    total_time = on_paper_time + in_air_time
    in_air_ratio = float(in_air_time / total_time) if total_time > 0 else 0.0

    # 2. Pause & Hesitation Analysis
    # Hesitation pauses during writing often reflect high cognitive load or motor planning deficit
    dx = np.diff(x)
    dy = np.diff(y)
    speeds = np.sqrt(dx**2 + dy**2) / (dt / 1000.0)

    is_pause = (speeds < pause_speed_threshold_px_s) & (pen_state[:-1] == 1)
    
    pause_count = 0
    total_pause_ms = 0.0
    current_pause_ms = 0.0

    for i in range(len(is_pause)):
        if is_pause[i]:
            current_pause_ms += dt[i]
        else:
            if current_pause_ms >= min_pause_duration_ms:
                pause_count += 1
                total_pause_ms += current_pause_ms
            current_pause_ms = 0.0
            
    if current_pause_ms >= min_pause_duration_ms:
        pause_count += 1
        total_pause_ms += current_pause_ms

    total_duration_s = max(total_time / 1000.0, 0.1)
    pause_rate = float(pause_count / total_duration_s)

    # 3. Pressure Dynamics
    mean_p = float(np.mean(pressure))
    std_p = float(np.std(pressure))
    dp = np.abs(np.diff(pressure))
    abrupt_pressure = int(np.sum(dp > 0.35))  # Spikes in grip tension

    return {
        "pen_lift_count": pen_lifts,
        "on_paper_time_ms": round(on_paper_time, 2),
        "in_air_time_ms": round(in_air_time, 2),
        "in_air_ratio": round(in_air_ratio, 4),
        "pause_count": pause_count,
        "total_pause_duration_ms": round(total_pause_ms, 2),
        "pause_rate_per_sec": round(pause_rate, 4),
        "mean_pressure": round(mean_p, 4),
        "pressure_std": round(std_p, 4),
        "abrupt_pressure_changes": abrupt_pressure
    }
