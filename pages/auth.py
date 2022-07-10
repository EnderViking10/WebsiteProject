import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..database import get_db, get_user_by_name, get_user_by_id, create_user, update_user
from ..forms import LoginForm, RegisterForm, ResetPasswordForm

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
        error = None

        if form.password.data != form.confirm.data:
            error = f"Passwords do not match"
            flash(error)
            return redirect(url_for('auth.register', form=form))

        try:
            create_user(form)
        except db.IntegrityError:
            error = f"User {form.username.data} is already registered."

        if error is None:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        error = None
        user = get_user_by_name(form.username.data)

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
        g.user = get_user_by_id(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    error = None
    if request.method == 'POST':
        if not check_password_hash(g.user['password'], form.old_password.data):
            error = 'Incorrect password.'

        if error is None:
            update_user(g.user['id'], generate_password_hash(form.new_password.data))
            return redirect(url_for('user.profile'))

        flash(error)

    return render_template('auth/reset_password.html', form=form)


@bp.route('/notAuthorized')
def not_authorized():
    return render_template('auth/not_authorized.html')
