from flask import Flask
import os
from dotenv import load_dotenv


def create_app():
    load_dotenv()
    my_app = Flask(__name__)

    my_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///features_prediction.db'
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_ALGORITHM"] = os.getenv("JWT_ALGORITHM", "HS256")
    app.config["JWT_EXP_DELTA_SECONDS"] = int(os.getenv("JWT_EXP_DELTA_SECONDS", "2524608000"))


if __name__ == '__main__':
    app.run()
