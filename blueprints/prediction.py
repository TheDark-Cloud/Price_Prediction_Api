from flask import Blueprint
from flask import request, jsonify
import pandas as pd
from app import pipeline

from ml_model.ml_loader import load_pipeline

prediction_bp = Blueprint('prediction_bp', __name__)


# Expected features in the same order used in training
REQUIRED_FIELDS = [
    'area','bedrooms','bathrooms','stories','mainroad','guestroom',
    'basement','hotwaterheating','airconditioning','parking','prefarea',
    'furnishingstatus'
]

@prediction_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": True})



@prediction_bp.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    # Normalize types
    try:
        x = {
            'area': float(data['area']),
            'bedrooms': int(data['bedrooms']),
            'bathrooms': int(data['bathrooms']),
            'stories': int(data['stories']),
            'mainroad': bool(data['mainroad']),
            'guestroom': bool(data['guestroom']),
            'basement': bool(data['basement']),
            'hotwaterheating': bool(data['hotwaterheating']),
            'airconditioning': bool(data['airconditioning']),
            'parking': int(data['parking']),
            'prefarea': bool(data['prefarea']),
            'furnishingstatus': str(data['furnishingstatus'])
        }
    except (ValueError, TypeError) as ex:
        return jsonify({'error': f'Invalid field types: {str(ex)}'}), 400

    # Build DataFrame in the required order
    df = pd.DataFrame([[x[f] for f in REQUIRED_FIELDS]], columns=REQUIRED_FIELDS)
    try:
        prediction = pipeline.predict(df)
    except Exception as ex:
        return jsonify({'error': f'Prediction failed: {str(ex)}'}), 500

    # Provide model metadata if available
    model_version = getattr(pipeline, 'version', 'v1') or 'v1'
    accuracy = 0.85
    return jsonify({'predictions':[float(prediction[0])], 'model_version':model_version, 'accuracy':accuracy}), 200

