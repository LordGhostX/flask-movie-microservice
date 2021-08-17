from flask import request, jsonify
from movie import app, db
from movie.models import Movie


@app.route("/movie/", methods=["POST"])
def add_movie():
    name = request.form.get("name")
    poster = request.form.get("poster")
    synopsis = request.form.get("synopsis")
    year_of_release = request.form.get("year_of_release")

    # check required args
    if any([name, poster]) is None:
        return jsonify({
            "msg": "name and poster are required arguments",
            "data": {}
        }), 400

    # check year is a valid integer
    if year_of_release:
        try:
            year_of_release = int(year_of_release)
        except ValueError:
            return jsonify({
                "msg": "year_of_release must be a valid integer",
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
