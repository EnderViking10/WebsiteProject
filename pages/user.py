from flask import (Blueprint, g, redirect, render_template, request, url_for)

from .auth import login_required
from ..database import create_ticket, get_all_tickets
from ..forms import CreateTicketForm, UserPageForm

bp = Blueprint('user', __name__)


@bp.route('/user/profile', methods=('GET', 'POST'))
@login_required
def profile():
    form = UserPageForm()
    if request.method == 'POST':
        return redirect(url_for('auth.reset_password'))

    return render_template('user/profile.html', form=form)


@bp.route('/user/tickets', methods=('GET', 'POST'))
@login_required
def tickets():
    all_tickets = get_all_tickets()
    ticket_list = list()
    for ticket in all_tickets:
        if ticket['author_id'] == g.user['id']:
            ticket_list.append(ticket)
    return render_template('user/tickets.html', tickets=ticket_list)


@bp.route('/user/create_ticket', methods=('GET', 'POST'))
@login_required
def ticket_create():
    form = CreateTicketForm()
    if request.method == 'POST':
        create_ticket(g.user['id'], form)
        return redirect(url_for('user.tickets'))

    return render_template('user/create_ticket.html', form=form)
