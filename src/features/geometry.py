"""
Geometric & Spatial Alignment Feature Extractor (ML-08).
Computes curvature, tortuosity, baseline alignment deviation, and spatial bounding metrics.
"""
from typing import List, Dict, Any
import numpy as np


def extract_geometric_features(stroke_points: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Computes curvature index, baseline drift angle, and bounding box dimensions.
    """
    default_geometry = {
        "tortuosity": 1.0,
        "mean_curvature": 0.0,
        "baseline_drift_degrees": 0.0,
        "bbox_width": 0.0,
        "bbox_height": 0.0,
        "bbox_aspect_ratio": 1.0,
        "spatial_dispersion": 0.0
    }

    if not stroke_points or len(stroke_points) < 4:
        return default_geometry

    x = np.array([p.get("x", 0.0) for p in stroke_points], dtype=float)
    y = np.array([p.get("y", 0.0) for p in stroke_points], dtype=float)

    # 1. Bounding Box & Aspect Ratio
    min_x, max_x = float(np.min(x)), float(np.max(x))
    min_y, max_y = float(np.min(y)), float(np.max(y))
    width = max(max_x - min_x, 1.0)
    height = max(max_y - min_y, 1.0)
    aspect_ratio = width / height

    # 2. Tortuosity (Path length / Euclidean displacement)
    dx = np.diff(x)
    dy = np.diff(y)
    path_length = float(np.sum(np.sqrt(dx**2 + dy**2)))
    euclidean_distance = float(np.sqrt((x[-1] - x[0])**2 + (y[-1] - y[0])**2))
    tortuosity = (path_length / euclidean_distance) if euclidean_distance > 1.0 else 1.0

    # 3. Curvature calculation along the curve: kappa = |x'y'' - y'x''| / (x'^2 + y'^2)^(3/2)
    curvatures = []
    if len(x) >= 5:
        dx_dt = np.gradient(x)
        dy_dt = np.gradient(y)
        d2x_dt2 = np.gradient(dx_dt)
        d2y_dt2 = np.gradient(dy_dt)
        denom = (dx_dt**2 + dy_dt**2)**(1.5)
        valid = denom > 1e-4
        if np.any(valid):
            num = np.abs(dx_dt[valid] * d2y_dt2[valid] - dy_dt[valid] * d2x_dt2[valid])
            curvatures = num / denom[valid]

    mean_curv = float(np.mean(curvatures)) if len(curvatures) > 0 else 0.0

    # 4. Baseline Alignment Drift
    # Linear regression fit through the stroke points to detect tilting baseline (common in dysgraphia)
    try:
        slope, _ = np.polyfit(x, y, 1)
        angle_rad = np.arctan(slope)
        drift_degrees = float(np.degrees(angle_rad))
    except Exception:
        drift_degrees = 0.0

    # 5. Spatial dispersion (spread around centroid)
    cx, cy = np.mean(x), np.mean(y)
    dispersion = float(np.mean(np.sqrt((x - cx)**2 + (y - cy)**2)))

    return {
        "tortuosity": round(min(tortuosity, 100.0), 4),
        "mean_curvature": round(min(mean_curv, 100.0), 4),
        "baseline_drift_degrees": round(abs(drift_degrees), 2),
        "bbox_width": round(width, 2),
        "bbox_height": round(height, 2),
        "bbox_aspect_ratio": round(aspect_ratio, 4),
        "spatial_dispersion": round(dispersion, 2)
    }
