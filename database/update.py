from werkzeug.security import generate_password_hash

from ._get_db import get_db
from ..forms import AdminUserForm, CreateItemForm, UpdateItemForm, RegisterForm, CreateTicketForm

"""
ITEM FUNCTIONS
"""


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
    db = get_db()  # Gets the database
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))  # Updates the item in the database
    db.commit()  # Commits the changes


"""
TICKET FUNCTIONS
"""


def create_ticket(author_id: int, form: CreateTicketForm) -> None:
    db = get_db()  # Gets the database
    # Updates the database
    db.execute(
        'INSERT INTO tickets'
        ' (author_id, title, description)'
        ' VALUES (?, ?, ?)',
        (author_id, form.title.data, form.description.data)
    )
    db.commit()  # Commits the changes


def delete_ticket(ticket_id: int) -> None:
    db = get_db()  # Gets the database
    db.execute('DELETE FROM tickets WHERE id = ?', (ticket_id,))  # Updates the item in the database
    db.commit()  # Commits the changes


"""
USER FUNCTIONS
"""


def create_user(form: RegisterForm) -> None:
    db = get_db()  # Gets the database
    # Updates the database
    db.execute(
        'INSERT INTO users'
        ' (username, password, user_level)'
        ' VALUES (?, ?, ?)',
        (form.username.data, generate_password_hash(form.password.data), 0)
    )
    db.commit()  # Commits the changes


def update_user(user_id: int, password: str) -> None:
    db = get_db()  # Gets the database
    # Updates the item in the database
    db.execute(
        'UPDATE users'
        ' SET (password)'
        ' = ?'
        ' WHERE id = ?',
        (password, user_id)
    )
    db.commit()  # Commits the changes


def admin_update_user(user_id: int, form: AdminUserForm) -> None:
    db = get_db()  # Gets the database
    # Updates the user  in the database
    db.execute(
        'UPDATE users'
        ' SET (user_level, restriction_level)'
        ' = (?, ?)'
        ' WHERE id = ?',
        (form.user_level.data, form.restriction_level.data, user_id)
    )
    db.commit()  # Commits the changes
