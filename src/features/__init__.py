"""
Feature extraction pipeline combining kinematics, events, and geometry into a comprehensive vector.
"""
from typing import List, Dict, Any
from .kinematics import extract_kinematic_features
from .stroke_events import extract_stroke_event_features
from .geometry import extract_geometric_features


def extract_all_stroke_features(stroke_points: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Extracts all 25+ kinematic, temporal, and geometric features from stroke data.
    """
    kinematics = extract_kinematic_features(stroke_points)
    events = extract_stroke_event_features(stroke_points)
    geometry = extract_geometric_features(stroke_points)

    combined = {}
    combined.update(kinematics)
    combined.update(events)
    combined.update(geometry)
    return combined
