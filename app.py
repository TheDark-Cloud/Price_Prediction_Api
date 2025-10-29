from flask import Flask
import os
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    my_app = Flask(__name__)

    my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///features_prediction.db'
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    my_app.register_blueprint(prediction_bp)


if __name__ == '__main__':
    app.run()
