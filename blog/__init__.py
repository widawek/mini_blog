from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    Create a shell context for the Flask application.

    This function adds specific objects to the shell context of Flask,
    facilitating work with the shell during debugging or interaction with
    the application.

    Returns:
        dict: A dictionary containing the 'db' and 'Entry' objects, which are
              made available in the Flask shell context.
    """
    return {
        "db": db,
        "Entry": models.Entry
    }

from blog import routes, models
