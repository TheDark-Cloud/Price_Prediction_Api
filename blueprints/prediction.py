from flask import Blueprint, request, jsonify, current_app, render_template
import pandas as pd

prediction_bp = Blueprint(
    'prediction_bp',
    __name__,
    template_folder='../templates',
    static_folder='../static'
)

REQUIRED_FIELDS = [
    'area','bedrooms','bathrooms','stories','mainroad','guestroom',
    'basement','hotwaterheating','airconditioning','parking','prefarea',
    'furnishingstatus'
]

ALLOWED_FURNISHING = {'furnished', 'semi-furnished', 'unfurnished'}

@prediction_bp.route("/health", methods=["GET"])
def health():
    loaded = current_app.config.get('MODEL_PIPELINE') is not None
    return jsonify({"status": "ok", "model_loaded": bool(loaded)}), 200

@prediction_bp.route("/api_prediction", methods=['POST'])
def predict_api():
    """
    JSON API endpoint.
    Expects application/json with keys matching REQUIRED_FIELDS.
    """
    try:
        data = request.get_json(force=True)
    except Exception as ex:
        return jsonify({'error': str(ex)}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({'error': f'Missing fields: {missing}'}), 400

    # furnishing validation
    furnishingstatus_str = str(data.get('furnishingstatus') or '').strip()
    if furnishingstatus_str not in ALLOWED_FURNISHING:
        return jsonify({'error': f'Invalid furnishingstatus: {furnishingstatus_str}. Must be one of {sorted(ALLOWED_FURNISHING)}'}), 400

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
            'furnishingstatus': furnishingstatus_str
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

@prediction_bp.route("/predict", methods=['GET', 'POST'])
def predict_page():
    """
    GET: render the single Jinja page with the form.
    POST: accept form-encoded data, validate, predict and re-render template with result.
    """
    if request.method == 'GET':
        return render_template('index.html', result=None)

    # POST (form submission)
    form = request.form.to_dict()
    missing = [f for f in REQUIRED_FIELDS if f not in form or form.get(f, "") == ""]
    if missing:
        return render_template('index.html', result={'error': f'Missing fields: {missing}'}), 400

    # validate furnishingstatus
    furnishingstatus_str = str(form.get('furnishingstatus') or '').strip()
    if furnishingstatus_str not in ALLOWED_FURNISHING:
        return render_template('index.html', result={'error': f'Invalid furnishingstatus: {furnishingstatus_str}. Must be one of {sorted(ALLOWED_FURNISHING)}'}), 400

    try:
        x = {
            'area': float(form['area']),
            'bedrooms': int(form['bedrooms']),
            'bathrooms': int(form['bathrooms']),
            'stories': int(form['stories']),
            'mainroad': form.get('mainroad') in ['1','true','True','on','yes'],
            'guestroom': form.get('guestroom') in ['1','true','True','on','yes'],
            'basement': form.get('basement') in ['1','true','True','on','yes'],
            'hotwaterheating': form.get('hotwaterheating') in ['1','true','True','on','yes'],
            'airconditioning': form.get('airconditioning') in ['1','true','True','on','yes'],
            'parking': int(form['parking']),
            'prefarea': form.get('prefarea') in ['1','true','True','on','yes'],
            'furnishingstatus': furnishingstatus_str
        }
    except (ValueError, TypeError) as ex:
        return render_template('index.html', result={'error': f'Invalid field types: {str(ex)}'}), 400

    df = pd.DataFrame([[x[f] for f in REQUIRED_FIELDS]], columns=REQUIRED_FIELDS)

    pipeline = current_app.config.get('MODEL_PIPELINE')
    if pipeline is None:
        price = x['area'] * 10 + x['bedrooms'] * 1000 - x['bathrooms'] * 200
        return render_template('index.html', result={'predictions': [float(price)], 'features': x})

    try:
        preds = pipeline.predict(df)
    except Exception as ex:
        current_app.logger.exception("Prediction failed")
        return render_template('index.html', result={'error': f'Prediction failed: {str(ex)}'}), 500

    return render_template('index.html', result={'predictions': [float(preds[0])], 'features': x})