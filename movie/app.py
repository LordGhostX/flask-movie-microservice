from movie import app, db
from movie.models import Movie
from movie.routes import add_movie

db.create_all()

if __name__ == "__main__":
    app.run()
