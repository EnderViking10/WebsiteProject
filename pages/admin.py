import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from ..database import admin_update_user, delete_ticket, get_all_tickets, get_all_users, get_user_by_id, get_user_by_name
from ..forms import AdminPageForm, AdminUserForm

bp = Blueprint('admin', __name__)


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['user_level'] < 1:
            return redirect(url_for('auth.not_authorized'))

        if g.user['restriction_level'] == 1:
            return redirect(url_for('auth.restricted'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/admin', methods=('GET', 'POST'))
@admin_required
def admin():
    form = AdminPageForm()
    if request.method == 'POST' and form.search.data:
        user = get_user_by_name(form.username.data)
        user_id = user['id']

        return redirect(url_for('admin.user_page', user_id=user_id))

    return render_template('admin/admin.html', form=form)


@bp.route('/user_list', methods=('GET', 'POST'))
@admin_required
def user_list():
    return render_template('admin/user_list.html', users=get_all_users())


@bp.route('/admin/user/<int:user_id>', methods=('GET', 'POST'))
@admin_required
def user_page(user_id: int):
    user = get_user_by_id(user_id)
    form = AdminUserForm()
    error = None

    if request.method == 'POST':
        if g.user['user_level'] < int(form.user_level.data):
            error = f"You are not authorized to do that"

        if error is None:
            admin_update_user(user_id, form)
            return redirect(url_for('admin.user_page', user_id=user_id))

        flash(error)

    return render_template('admin/admin_user.html', user=user, form=form)


@bp.route('/admin/tickets', methods=['GET', 'POST'])
@admin_required
def tickets():
    ticket_list = get_all_tickets()
    users = get_all_users()
    return render_template('admin/admin_tickets.html', tickets=ticket_list, users=users)


@bp.route('/admin/delete_ticket/<int:ticket_id>', methods=('GET', 'POST'))
@admin_required
def ticket_delete(ticket_id):
    delete_ticket(ticket_id)
    return redirect(url_for('admin.tickets'))
