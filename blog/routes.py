from flask import render_template, request, flash, session, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get('logged_in'):
            return view_func(*args, **kwargs)
        return redirect(url_for('login', next=request.path))
    return check_permissions


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True)\
        .order_by(Entry.pub_date.desc())

    return render_template("homepage.html", all_posts=all_posts)


@app.route("/post/<int:entry_id>", methods=["GET", "POST"])
@app.route("/post/", defaults={'entry_id': None}, methods=["GET", "POST"])
@login_required
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


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get('next')
    if request.method == 'POST':
        if form.validate_on_submit():
            session['logged_in'] = True
            session.permanent = True  # Use cookie to store session.
            flash('You are now logged in.', 'success')
            return redirect(next_url or url_for('index'))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False)\
        .order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@app.route("/post/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Wpis został usunięty.', 'success')
    return redirect(url_for('index'))
