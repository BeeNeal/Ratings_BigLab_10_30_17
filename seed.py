"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User, Movie, Rating

from model import connect_to_db, db
from server import app

import datetime


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # Add to the session to be stored.
        db.session.add(user)

    # Add to database.
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate movies.
    Movie.query.delete()

    for row in open("seed_data/u.item"):
        row = row.rstrip()
        movie_data = row.split("|")
        movie_id = movie_data[0]
        title = movie_data[1][:-7]  # Slice off parenthetical date in title.
        imdb_url = movie_data[4]

        released_str = movie_data[2]  # Save date string.

        # If date string (Truthy).
        if released_str:
            # Convert date string to datetime object, save to variable.
            released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        # Otherwise, make equal to None.
        else:
            released_at = None

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        # Add to the session to be stored.
        db.session.add(movie)

    # Add to database.
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate ratings.
    Rating.query.delete()
    query = "SELECT setval('ratings_rating_id_seq', 1)"
    db.session.execute(query)
    db.session.commit()

    for row in open("seed_data/u.data"):
        row = row.rstrip()
        rating_data = row.split("\t")

        movie_id = rating_data[0]
        user_id = rating_data[1]
        score = rating_data[2]

        rating = Rating(movie_id=movie_id,
                        user_id=user_id,
                        score=score)
        # Add to the session to be stored.
        db.session.add(rating)

    # Add to database.
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    # We are adjusting the users_user_id_seq, using the Postgres function setval.
    set_val_user_id()
