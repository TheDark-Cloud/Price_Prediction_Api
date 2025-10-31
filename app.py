from dotenv import load_dotenv
from flask import Flask, send_from_directory
import os
from setting.init_db import database
from blueprints.prediction import prediction_bp
from ml_model.ml_loader import load_pipeline  # loader returns pipeline object or None
from flask_migrate import Migrate

load_dotenv()
db_migrate = Migrate()

def create_app():
    my_app = Flask(__name__)

    my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    # init db
    database.init_app(my_app)
    db_migrate.init_app(my_app, database)

    # loading the model pipeline once and store in config
    pipeline = load_pipeline()  # safe: loader should handle missing file and return None
    my_app.config['MODEL_PIPELINE'] = pipeline

    # register blueprint
    my_app.register_blueprint(prediction_bp)

    @my_app.route('/Price_Prediction_Api/')
    def serve_index_prefixed():
        root = os.path.abspath(os.path.dirname(__file__))
        return send_from_directory(root, 'index.html')

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