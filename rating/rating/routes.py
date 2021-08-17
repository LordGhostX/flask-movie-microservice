from flask import request, jsonify
from rating import app, db
from rating.models import Rating
from rating.utils import validate_rating


@app.route("/rating/", methods=["POST"])
def add_rating():
    movie_id = request.form.get("id")
    rating_value = request.form.get("rating")
    review = request.form.get("review")

    # check required args
    if None in [movie_id, rating_value]:
        return jsonify({
            "msg": "movie ID and rating_value are required arguments",
            "data": {}
        }), 400

    # review must be within 1 - 5
    try:
        rating_value = validate_rating(rating_value)
    except ValueError:
        return jsonify({
            "msg": "rating_value must be either 1, 2, 3, 4 or 5",
            "data": {}
        }), 400

    # save the details in the database
    rating = Rating(
        movie_id=movie_id,
        rating_value=rating_value,
        review=review
    )
    db.session.add(rating)
    db.session.commit()

    return jsonify({
        "msg": "successfully added movie rating",
        "data": {}
    }), 201


@app.route("/rating/", methods=["GET"])
def get_rating():
    movie_id = request.form.get("id")

    if movie_id is None:
        return jsonify({
            "msg": "movie ID is a required argument",
            "data": {}
        }), 400

    movie_rating = db.engine.execute(
        "SELECT AVG(rating_value) FROM movies WHERE movie_id=?", movie_id).fetchone()
    return jsonify({
        "msg": "successfully fetched movie rating",
        "data": {
            "rating_value": movie_rating[0]
        }
    })
