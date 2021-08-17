from functools import wraps
from datetime import datetime
from flask import request, jsonify
from movie import app, db
from movie.models import Movie
from movie.utils import validate_year


def requested_movie_exists(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        movie_id = request.args.get("id")

        # check required args
        if movie_id is None:
            return jsonify({
                "msg": "movie ID is a required argument",
                "data": {}
            }), 400

        # check if the movie exists
        movie = Movie.query.get(movie_id)
        if movie is None:
            return jsonify({
                "msg": "the requested movie does not exist",
                "data": {}
            }), 404

        return f(movie, *args, **kwargs)
    return decorated


@app.route("/movie/", methods=["POST"])
def add_movie():
    name = request.form.get("name")
    poster = request.form.get("poster")
    synopsis = request.form.get("synopsis")
    year_of_release = request.form.get("year_of_release")

    # check required args
    if None in [name, poster]:
        return jsonify({
            "msg": "name and poster are required arguments",
            "data": {}
        }), 400

    # check year is a valid
    try:
        year_of_release = validate_year(year_of_release)
    except ValueError:
        return jsonify({
            "msg": "year_of_release must be a valid positive integer",
            "data": {}
        }), 400

    # save the details in the database
    movie = Movie(
        name=name,
        poster=poster,
        synopsis=synopsis,
        year_of_release=year_of_release
    )
    db.session.add(movie)
    db.session.commit()

    return jsonify({
        "msg": "successfully added new movie",
        "data": {}
    }), 201


@app.route("/movie/", methods=["GET"])
@requested_movie_exists
def get_movie(movie):
    return jsonify({
        "msg": "successfully fetched movie details",
        "data": {
            "id": movie.id,
            "name": movie.name,
            "poster": movie.poster,
            "synopsis": movie.synopsis,
            "year_of_release": movie.year_of_release,
            "last_updated": movie.last_updated,
            "date_created": movie.date_created
        }
    }), 200


@app.route("/movie/", methods=["DELETE"])
@requested_movie_exists
def delete_movie(movie):
    db.session.delete(movie)
    db.session.commit()

    return jsonify({
        "msg": "successfully deleted movie details",
        "data": {}
    }), 200


@app.route("/movie/", methods=["PUT"])
@requested_movie_exists
def update_movie(movie):
    name = request.form.get("name", movie.name)
    poster = request.form.get("poster", movie.poster)
    synopsis = request.form.get("synopsis", movie.synopsis)
    year_of_release = request.form.get(
        "year_of_release", movie.year_of_release)

    # check year is a valid
    try:
        year_of_release = validate_year(year_of_release)
    except ValueError:
        return jsonify({
            "msg": "year_of_release must be a valid positive integer",
            "data": {}
        }), 400

    movie.name = name
    movie.poster = poster
    movie.synopsis = synopsis
    movie.year_of_release = year_of_release
    movie.last_updated = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "msg": "successfully updated movie details",
        "data": {}
    }), 200


@app.route("/movies/", methods=["GET"])
def get_all_movies():
    movies = []
    for movie in Movie.query.all():
        movies.append({
            "id": movie.id,
            "name": movie.name,
            "poster": movie.poster,
            "synopsis": movie.synopsis,
            "year_of_release": movie.year_of_release,
            "last_updated": movie.last_updated,
            "date_created": movie.date_created
        })
    return jsonify({
        "msg": "successfully fetched all movies",
        "data": movies
    }), 200
