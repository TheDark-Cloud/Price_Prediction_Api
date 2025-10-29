from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

class Features(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    pass