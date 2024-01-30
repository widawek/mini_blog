from . import db
import datetime


class Entry(db.Model):
    """
    Database model for a blog entry.

    Represents a blog post or entry in the database with various fields
    including title, body, publication date, and publication status.
    Inherits from db.Model, indicating that it is a SQLAlchemy model.

    Attributes:
        id (int): Unique identifier for the blog entry, serves as the primary key.
        title (str): Title of the blog entry, limited to 80 characters, cannot be null.
        body (Text): The main content of the blog entry, cannot be null.
        pub_date (DateTime): Date and time the blog entry was published, defaults to current time.
        is_published (bool): Boolean flag indicating whether the entry is published, defaults to False.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
