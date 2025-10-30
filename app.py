from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from blueprints.prediction import prediction_bp
from setting.init_db import db


def create_app():
    load_dotenv()
    my_app = Flask(__name__)

    my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///features_prediction.db'
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    my_app.register_blueprint(prediction_bp)

    db = SQLAlchemy(my_app)

    return my_app

if __name__ == '__main__':
    try:
        app = create_app()
        db.create_all()

        app.run(debug=True)
        # app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print({"INTERNAL ERROR": str(e)})