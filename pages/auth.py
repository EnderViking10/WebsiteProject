import functools
import random
import string

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash

from ..database import create_user, get_db, get_user_by_id, get_user_by_name, update_user
from ..forms import LoginForm, RegisterForm, ResetPasswordForm
from ..forms.auth.forgot_password import ForgotPasswordForm

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        if g.user['restriction_level'] == 1:
            return redirect(url_for('auth.restricted'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


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
            character_list = string.ascii_letters + string.digits + string.punctuation
            backup_code = ''.join(random.choice(character_list) for i in range(8))
            create_user(form, backup_code)
        except db.IntegrityError:
            error = f"User {form.username.data} is already registered."

        if error is None:
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.log_in.data:
        error = None
        user = get_user_by_name(form.username.data)

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], form.password.data):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    if request.method == 'POST' and form.forgot_password.data:
        return redirect(url_for('auth.forgot_password'))

    return render_template('auth/login.html', form=form)


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

        if form.new_password.data != form.confirm.data:
            error = f"Passwords do not match"

        if error is None:
            character_list = string.ascii_letters + string.digits + string.punctuation
            new_backup_code = ''.join(random.choice(character_list) for i in range(8))
            update_user(g.user['id'], form.new_password.data, new_backup_code)
            return redirect(url_for('user.profile'))

        flash(error)

    return render_template('auth/reset_password.html', form=form)


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    error = None
    if request.method == 'POST':
        user = get_user_by_name(form.username.data)
        if user is None:
            error = f'User {form.username.data} was not found'
        elif user['backup_code'] != form.backup_code.data:
            error = 'Incorrect backup code'
        elif form.password.data != form.confirm.data:
            error = f"Passwords do not match"
        elif error is None:
            character_list = string.ascii_letters + string.digits + string.punctuation
            new_backup_code = ''.join(random.choice(character_list) for i in range(8))
            update_user(user['id'], form.password.data, new_backup_code)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/forgot_password.html', form=form)


@bp.route('/notAuthorized')
def not_authorized():
    return render_template('auth/not_authorized.html')


@bp.route('/restricted')
def restricted():
    return render_template('auth/restricted.html')
