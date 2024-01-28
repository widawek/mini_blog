from flask import render_template, request, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True)\
        .order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
@app.route("/post/", defaults={'entry_id': None}, methods=["GET", "POST"])
def post(entry_id):
    entry = None
    if entry_id:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        flash_text = 'Post został pomyślnie zaktualizowany!'

    else:
        form = EntryForm()
        entry = Entry(
                title=form.title.data,
                body=form.body.data,
                is_published=form.is_published.data
            )
        flash_text = 'Post został dodany pomyślnie!'

    errors = None
    if request.method == "POST":
        if form.validate_on_submit():
            if entry_id:
                form.populate_obj(entry)
                db.session.commit()
            else:
                db.session.add(entry)
                db.session.commit()
            flash(flash_text, 'success')
    else:
        errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)
