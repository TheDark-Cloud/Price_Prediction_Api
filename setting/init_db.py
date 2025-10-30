from flask_sqlalchemy import SQLAlchemy

database: SQLAlchemy = SQLAlchemy()

class Features(database.Model):
    __tablename__ = 'features'
    id = database.Column(database.Integer, primary_key=True)
    area = database.Column(database.Float)
    bedrooms = database.Column(database.Integer)
    bathrooms = database.Column(database.Integer)
    stories = database.Column(database.Integer)
    mainroad = database.Column(database.Boolean)
    guestroom = database.Column(database.Boolean)
    basement = database.Column(database.Boolean)
    hotwaterheating = database.Column(database.Boolean)
    airconditioning = database.Column(database.Boolean)
    parking = database.Column(database.Integer)
    prefarea = database.Column(database.Boolean)
    furnishingstatus = database.Column(database.String(20))
    prediction = database.Column(database.Float)


furnished_categories = ['furnished' 'semi-furnished' 'unfurnished']