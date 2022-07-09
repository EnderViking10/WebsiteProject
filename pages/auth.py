import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import get_db
from flaskr.forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if request.method == 'POST':
        db = get_db()

        try:
            db.execute(
                "INSERT INTO user (username, password, user_level) VALUES (?, ?, ?)",
                (form.username.data, generate_password_hash(form.password.data), 0)
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {form.username.data} is already registered."
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (form.username.data,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], form.password.data):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/notAuthorized')
def not_authorized():
    return render_template('auth/not_authorized.html')
