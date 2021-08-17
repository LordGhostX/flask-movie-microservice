from datetime import datetime
from rating import db


class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=True)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
