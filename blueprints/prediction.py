from flask import Blueprint
from flask import request, jsonify
import pandas as pd

from ml_model.ml_loader import load_pipeline

prediction_bp = Blueprint('prediction_bp', __name__)


# Expected features in the same order used in training
EXPECTED_FEATURES = [
    'area','bedrooms','bathrooms','stories','mainroad','guestroom',
    'basement','hotwaterheating','airconditioning','parking','prefarea',
    'furnishingstatus'
]

@prediction_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": True})



@prediction_bp.route("/predict", methods=["POST"])
def predict():
    # Parse JSON body
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    # Accept the single record or list
    records = payload if isinstance(payload, list) else [payload]

    # Build DataFrame
    try:
        df = pd.DataFrame(records)
    except Exception:
        return jsonify({"error": "Payload must be an object or list of objects"}), 400

    # Check missing features
    missing = [f for f in EXPECTED_FEATURES if f not in df.columns]
    if missing:
        return jsonify({"error": f"Missing required features: {missing}"}), 400

    # Keep only expected features and in th same order
    X = df[EXPECTED_FEATURES].copy()

    # Basic numeric coercion for numeric columns
    numeric_cols = ['area','bedrooms','bathrooms','stories','parking']
    for col in numeric_cols:
        X[col] = pd.to_numeric(X[col], errors='coerce')

    if X[numeric_cols].isnull().any().any():
        return jsonify({"error": "Numeric features must be valid numbers"}), 400

    # Predict
    try:
        preds = pipeline.predict(X)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    # Return float casted predictions
    return jsonify({"predictions": [float(p) for p in preds]})
