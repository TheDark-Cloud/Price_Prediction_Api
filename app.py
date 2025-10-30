from dotenv import load_dotenv
from flask import Flask
import os
from setting.init_db import database
from blueprints.prediction import prediction_bp
from ml_model.ml_loader import load_pipeline  # loader returns pipeline object or None

load_dotenv()

def create_app():
    my_app = Flask(__name__)

    my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # init db
    database.init_app(my_app)

    # loading the model pipeline once and store in config
    pipeline = load_pipeline()  # safe: loader should handle missing file and return None
    my_app.config['MODEL_PIPELINE'] = pipeline

    # register blueprint
    my_app.register_blueprint(prediction_bp)

    return my_app

if __name__ == '__main__':
    try:
        app = create_app()
        # create tables within the app context
        with app.app_context():
            database.create_all()
        app.run(debug=True)  # for production replace it with the WSGI server
    except Exception as e:
        print({"INTERNAL ERROR": str(e)})