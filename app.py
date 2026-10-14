"""
Nexus AI/ML Flask REST API Service (ML-20, ML-21, ML-22, ML-23, ML-25).
Provides screening prediction and feature analysis endpoints for Frontend and Spring Boot Backend.
"""
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

from config import FLASK_HOST, FLASK_PORT, DEBUG_MODE
from src.service.predictor import NexusPredictor

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
)
logger = logging.getLogger("NexusML")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin requests for React frontend and Spring Boot

# Initialize Predictor singleton
predictor = NexusPredictor()
try:
    predictor.initialize()
    logger.info("NexusPredictor initialized successfully.")
except Exception as e:
    logger.warning(f"Predictor initialized with default fallback: {e}")


@app.route("/", methods=["GET"])
def index():
    """API Root documentation."""
    return jsonify({
        "service": "Nexus Screening Intelligence AI/ML Service",
        "status": "ONLINE",
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "analysis": "POST /api/analysis"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Docker / orchestration."""
    return jsonify({
        "status": "UP",
        "models_loaded": predictor.is_initialized
    }), 200


@app.route("/predict", methods=["POST"])
@app.route("/api/analysis", methods=["POST"])
def predict():
    """
    Main Screening Inference Endpoint (ML-21, BE-25).
    Accepts assessment results and stroke coordinate streams, returns clinical evidence level.
    """
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({
                "error": "Bad Request",
                "message": "Missing JSON body. Payload must be valid JSON."
            }), 400

        # Input Validation (ML-25)
        age = data.get("age_years")
        if age is not None:
            try:
                age_val = float(age)
                if age_val < 3 or age_val > 18:
                    return jsonify({
                        "error": "Validation Error",
                        "message": "age_years must be between 3 and 18."
                    }), 422
            except (ValueError, TypeError):
                return jsonify({
                    "error": "Validation Error",
                    "message": "age_years must be a valid numeric value."
                }), 422

        # Run inference pipeline
        result = predictor.predict(data)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Inference error: {str(e)}", exc_info=True)
        return jsonify({
            "error": "Internal Server Error",
            "message": str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found", "message": "The requested endpoint does not exist."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed", "message": "HTTP method not supported on this route."}), 405


if __name__ == "__main__":
    logger.info(f"Starting Nexus AI/ML Service on {FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=DEBUG_MODE)
