def validate_year(year):
    if year:
        year = int(year)
        if year <= 0:
            raise ValueError

    return year
