# blueprints/prediction.py
from flask import Blueprint, request, jsonify, current_app
import pandas as pd

prediction_bp = Blueprint('prediction_bp', __name__)

REQUIRED_FIELDS = [
    'area','bedrooms','bathrooms','stories','mainroad','guestroom',
    'basement','hotwaterheating','airconditioning','parking','prefarea',
    'furnishingstatus'
]

@prediction_bp.route("/health", methods=["GET"])
def health():
    loaded = current_app.config.get('MODEL_PIPELINE') is not None
    return jsonify({"status": "ok", "model_loaded": bool(loaded)}), 200

@prediction_bp.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({'error': 'Invalid JSON'}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

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

    df = pd.DataFrame([[x[f] for f in REQUIRED_FIELDS]], columns=REQUIRED_FIELDS)

    pipeline = current_app.config.get('MODEL_PIPELINE')
    if pipeline is None:
        # development fallback: simple formula
        price = x['area'] * 10 + x['bedrooms'] * 1000 - x['bathrooms'] * 200
        return jsonify({'predictions': [float(price)]}), 200

    try:
        preds = pipeline.predict(df)
    except Exception as ex:
        current_app.logger.exception("Prediction failed")
        return jsonify({'error': f'Prediction failed: {str(ex)}'}), 500

    return jsonify({'predictions': [float(preds[0])]}), 200