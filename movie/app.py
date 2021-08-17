from movie import app, db
from movie.models import Movie
from movie.routes import add_movie, get_movie, update_movie, delete_movie, get_all_movies

db.create_all()

if __name__ == "__main__":
    app.run()
