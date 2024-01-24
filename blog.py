from blog import app, db
from blog import models


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "Entry": models.Entry
    }


if __name__ == "__main__":
    app.run()
