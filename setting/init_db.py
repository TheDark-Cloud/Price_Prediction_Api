from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

class Features(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.Float)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    stories = db.Column(db.Integer)
    mainroad = db.Column(db.Boolean)
    guestroom = db.Column(db.Boolean)
    basement = db.Column(db.Boolean)
    hotwaterheating = db.Column(db.Boolean)
    airconditioning = db.Column(db.Boolean)
    parking = db.Column(db.Integer)
    prefarea = db.Column(db.Boolean)
    furnishingstatus = db.Column(db.String(20))


furnished_categories = ['furnished' 'semi-furnished' 'unfurnished']