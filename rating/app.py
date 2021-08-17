from rating import app, db
from rating.models import Rating
from rating.routes import add_rating, get_rating

db.create_all()

if __name__ == "__main__":
    app.run()
