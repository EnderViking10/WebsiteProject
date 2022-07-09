import functools

from flask import (
    Blueprint, redirect, render_template, request, url_for, g
)

from ..database import get_user_by_id, get_user_by_name, admin_update_user
from ..forms import AdminSearchForm, AdminUserForm

bp = Blueprint('admin', __name__)


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['user_level'] < 1:
            return redirect(url_for('auth.not_authorized'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/admin', methods=('GET', 'POST'))
@admin_required
def admin():
    form = AdminSearchForm()
    if request.method == 'POST':
        user = get_user_by_name(form.username.data)
        user_id = user['id']

        return redirect(url_for('admin.user_page', user_id=user_id))

    return render_template('admin/admin.html', form=form)


@bp.route('/admin/user/<int:user_id>', methods=('GET', 'POST'))
@admin_required
def user_page(user_id):
    user = get_user_by_id(user_id)
    form = AdminUserForm()

    if request.method == 'POST':
        admin_update_user(user_id, form)
        return redirect(url_for('admin.user_page', user_id=user_id))

    return render_template('admin/user_page.html', user=user, form=form)
