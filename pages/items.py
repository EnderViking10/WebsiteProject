from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from flaskr.forms import UpdateItemForm, CreateItemForm
from .auth import login_required
from ..database import update_item, get_all_items, get_item, delete_item, create_item

bp = Blueprint('items', __name__)


@bp.route('/items')
def items():
    item_list = get_all_items()
    return render_template('items/items.html', items=item_list)


@bp.route('/items/create', methods=('GET', 'POST'))
@login_required
def create():
    form = CreateItemForm()
    if request.method == 'POST':
        create_item(form)
        return redirect(url_for('items.items'))

    return render_template('items/create.html', form=form)


@bp.route('/items/update/<int:item_id>', methods=('GET', 'POST'))
def update(item_id):
    item = get_item(item_id)
    form = UpdateItemForm()

    if request.method == 'POST':
        update_item(item_id, form)
        return redirect(url_for('items.items'))

    return render_template('items/update.html', item=item, form=form)


@bp.route('/items/delete/<int:item_id>', methods=('POST',))
@login_required
def delete(item_id):
    delete_item(item_id)
    return redirect(url_for('items.items'))
