"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64),
                      unique=True,
                      nullable=True)
    password = db.Column(db.String(64),
                         nullable=True)
    age = db.Column(db.Integer,
                    nullable=True)
    zipcode = db.Column(db.String(15),
                        nullable=True)

    def __repr__(self):
        """Provide helpful information about user when printed."""

        s = "<User user_id=%s email=%s>"
        return s % (self.user_id, self.email)


class Movie(db.Model):
    """List of movies with movie data."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    title = db.Column(db.String(128),
                      nullable=False)
    released_at = db.Column(db.DateTime,
                            nullable=True)
    imdb_url = db.Column(db.String(200),
                         nullable=True)

    def __repr__(self):
        """Provide helpful information about movie when printed."""

        s = "<Movie movie_id=%s title=%s>"
        return s % (self.movie_id, self.title)


class Rating(db.Model):
    """List of user rating data."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)
    movie_id = db.Column(db.Integer,
                         db.ForeignKey('movies.movie_id'),
                         nullable=False)
    # Column/field is an integer, and also declared as a Foreign Key to
    # reference another column in another table. The user_id column of ratings
    # refers to the user_id column of users.
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),  # The parameter passed to ForeignKey() should be a string in the format of “table.column_name”.
                        nullable=False)
    score = db.Column(db.Integer,
                      nullable=False)

    # Define relationship between Rating and Movie objects.
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))

    # Define relationship between Rating and User.
    # The relationship adds an attribute on ratings objects called 'user', the
    # value of which is the same as if you had queried the users table directly.
    # Furthermore, a user object now has an attribute named 'ratings', which is
    # a list of all the ratings associated with that user, simultaneously
    # queried from the database.
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    def __repr__(self):
        """Provide helpful information about rating when printed."""

        s = "<Rating rating_id=%d movie_id=%d user_id=%d score=%d>"
        return s % (self.rating_id,
                    self.movie_id,
                    self.user_id,
                    self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
