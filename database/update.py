from . import get_item
from ._get_db import get_db
from ..forms import AdminUserForm, CreateItemForm, UpdateItemForm


def create_item(form: CreateItemForm) -> None:
    db = get_db()  # Gets the database
    # Updates the database
    db.execute(
        'INSERT INTO items'
        ' (name, description, cost)'
        ' VALUES (?, ?, ?)',
        (form.name.data, form.description.data, form.cost.data)
    )
    db.commit()  # Commits the changes


def update_item(item_id: int, form: UpdateItemForm) -> None:
    db = get_db()  # Gets the database
    # Updates the item in the database
    db.execute(
        'UPDATE items'
        ' SET (name, description, cost)'
        ' = (?, ?, ?)'
        ' WHERE id = ?',
        (form.name.data, form.description.data, form.cost.data, item_id)
    )
    db.commit()  # Commits the changes


def delete_item(item_id: int) -> None:
    get_item(item_id)
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()


def admin_update_user(user_id: int, form: AdminUserForm) -> None:
    db = get_db()  # Gets the database
    # Updates the user  in the database
    db.execute(
        'UPDATE user'
        ' SET user_level'
        ' = ?'
        ' WHERE id = ?',
        (form.user_level.data, user_id)
    )
    db.commit()  # Commits the changes
