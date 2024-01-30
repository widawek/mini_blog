from flask import render_template, request, flash, session, redirect, url_for
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm, LoginForm
import functools


def login_required(view_func):
    """
    Decorator for routes that require login.

    Checks if a user is logged in by verifying the 'logged_in' key in the session.
    If the user is not logged in, redirects to the login page.

    Args:
        view_func (function): The view function to be decorated.

    Returns:
        function: The decorated view function with login check.
    """

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
    """
    Route for adding a new post or editing an existing post.

    When accessed with GET, displays a form for adding or editing a post.
    When accessed with POST, processes the submitted form and adds/updates the post.

    Args:
        entry_id (int): The ID of the entry to edit; if None, a new entry is created.

    Returns:
        Rendered template: The entry form template for adding or editing posts.
    """

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
    """
    Login route.

    Handles user authentication. On GET, displays the login form.
    On POST, processes the login form and authenticates the user.

    Returns:
        Rendered template or redirect: The login form template or a redirect to
        another page upon successful login.
    """

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
    """
    Logout route.

    Logs out the user and clears the session.

    Returns:
        Redirect: A redirect to the homepage.
    """

    if request.method == 'POST':
        session.clear()
        flash('You are now logged out.', 'success')
    return redirect(url_for('index'))


@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
    """
    Drafts route.

    Displays a list of unpublished blog posts (drafts).

    Returns:
        Rendered template: The template showing all draft posts.
    """

    drafts = Entry.query.filter_by(is_published=False)\
        .order_by(Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@app.route("/post/delete/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    """
    Route to delete a blog post.

    Deletes the post with the specified entry_id.

    Args:
        entry_id (int): The ID of the entry to be deleted.

    Returns:
        Redirect: A redirect to the homepage with a flash message indicating success or failure.
    """

    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Wpis został usunięty.', 'success')
    return redirect(url_for('index'))
