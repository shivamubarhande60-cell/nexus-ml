"""
API Test Script for Nexus AI/ML Service (ML-24).
Tests /health, /predict, and /api/analysis endpoints with typical and risk test cases.
"""
import json
import unittest
from app import app


class TestNexusMLAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_check(self):
        """Test GET /health endpoint."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "UP")

    def test_typical_child_screening(self):
        """Test POST /predict with typical developing metrics."""
        payload = {
            "child_id": "child-101",
            "age_years": 7.5,
            "grade": 2,
            "phonology_accuracy": 0.92,
            "phonology_latency_ms": 1100,
            "rapid_naming_speed": 3.2,
            "reading_accuracy": 0.90,
            "working_memory_score": 0.85,
            "stroke_points": [
                {"x": 10.0, "y": 10.0, "t": 100, "pressure": 0.5, "pen_state": 1},
                {"x": 20.0, "y": 25.0, "t": 200, "pressure": 0.52, "pen_state": 1},
                {"x": 35.0, "y": 40.0, "t": 300, "pressure": 0.51, "pen_state": 1},
                {"x": 50.0, "y": 55.0, "t": 400, "pressure": 0.49, "pen_state": 1},
                {"x": 70.0, "y": 70.0, "t": 500, "pressure": 0.50, "pen_state": 1}
            ]
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("evidence_level", data)
        self.assertIn("composite_score", data)
        self.assertIn("confidence", data)
        self.assertIn("top_contributing_features", data)

    def test_elevated_concern_screening(self):
        """Test POST /api/analysis with elevated concern indicators."""
        payload = {
            "child_id": "child-202",
            "age_years": 8.0,
            "grade": 2,
            "phonology_accuracy": 0.42,
            "phonology_latency_ms": 2900,
            "rapid_naming_speed": 1.1,
            "reading_accuracy": 0.45,
            "working_memory_score": 0.50,
            "stroke_features": {
                "mean_velocity": 55.0,
                "normalized_jerk": 78.0,
                "pen_lift_count": 14,
                "in_air_ratio": 0.42,
                "pause_rate_per_sec": 0.85,
                "mean_pressure": 0.80,
                "pressure_std": 0.25,
                "tortuosity": 1.75,
                "baseline_drift_degrees": 12.0
            }
        }
        res = self.client.post("/api/analysis", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["evidence_level"], "ELEVATED_CONCERN")
        self.assertGreaterEqual(data["composite_score"], 0.70)

    def test_insufficient_evidence_fallback(self):
        """Test fallback trigger when completion ratio is low (ML-17)."""
        payload = {
            "child_id": "child-303",
            "age_years": 6.0,
            "task_completion_ratio": 0.20,  # Below 0.40 threshold
            "stroke_points": []
        }
        res = self.client.post("/predict", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["evidence_level"], "INSUFFICIENT_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
