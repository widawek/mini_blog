from faker import Faker
from blog import app
from blog.models import Entry, db


def generate_entries(how_many=10):
    fake = Faker()

    for i in range(how_many):
        post = Entry(
            title=fake.sentence(),
            body='\n'.join(fake.paragraphs(15)),
            is_published=True
        )
        db.session.add(post)
    db.session.commit()


if __name__ == '__main__':
    app_context = app.app_context()
    app_context.push()

    with app.app_context():
        generate_entries()

    app_context.pop()
