from datetime import datetime
from movie import db


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    poster = db.Column(db.String, nullable=False)
    synopsis = db.Column(db.String, nullable=True)
    year_of_release = db.Column(db.Integer, nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
