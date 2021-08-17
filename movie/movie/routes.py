from functools import wraps
from flask import request, jsonify
from movie import app, db
from movie.models import Movie


def requested_movie_exists(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        movieID = request.args.get("id")

        # check required args
        if movieID is None:
            return jsonify({
                "msg": "movie ID is a required argument",
                "data": {}
            }), 400

        # check if the movie exists
        movie = Movie.query.get(movieID)
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

    # check year is a valid integer
    if year_of_release:
        try:
            year_of_release = int(year_of_release)
            if year_of_release <= 0:
                raise ValueError
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
