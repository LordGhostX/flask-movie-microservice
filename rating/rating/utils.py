def validate_rating(rating):
    rating = int(rating)
    if rating < 1 or rating > 5:
        raise ValueError

    return rating
