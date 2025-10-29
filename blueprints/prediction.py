from flask import Blueprint
from flask import request, jsonify
from setting.token_auth import create_encoded_token, token_required, decode_token


prediction_bp = Blueprint('prediction_bp', __name__)


@prediction_bp.route("/home-price-prediction-data", methods=["GET"])
def fetch_data():
    """Getting the datat from the users, which will be used for prediction later"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400

        payload = create_encoded_token(data.jsonify())
        return payload, 200
    except Exception as ex:
        return jsonify({"message": str(ex)}), 500

    # sample of a response: {"features" : [a1, a1, a3, ..., a7]


@prediction_bp.route("/your home price prediction", methods=["POST"])
@token_required
def predict(token):
    try:
        if not token:
            return jsonify({"message": "No token provided"}), 400

        if isinstance(token, str):
            return jsonify({"message": "Wrong token formatting"}), 400


        payload = decode_token(token) # decoding the token
        if not payload:
            return jsonify({"message": "Invalid token"}), 400

        model_feature = []
        for key, value in payload.items():
            model_feature.append(value)


    except Exception as ex:
        return jsonify({"message": str(ex)}), 500
