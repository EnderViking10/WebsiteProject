from werkzeug.exceptions import abort

from ._get_db import get_db


def get_all_items() -> list:
    """ Gets all the items in the database"""
    db = get_db()  # Gets the database
    items = db.execute(
        'SELECT *'
        ' FROM items'
        ' ORDER BY id DESC'
    ).fetchall()  # Gets the items

    return items  # Returns the items


def get_item(item_id: int) -> any:
    """ Gets a single item """
    db = get_db()  # Gets the database
    item = db.execute(
        'SELECT *'
        ' FROM items'
        ' WHERE id = ?',
        (item_id,)
    ).fetchone()  # Gets the single item

    if item is None:
        abort(404, f"Item {item} was not found.")

    return item  # Returns the item


"""
TICKET FUNCTIONS
"""


def get_all_tickets() -> list:
    """ Gets all the tickets in the database"""
    db = get_db()  # Gets the database
    tickets = db.execute(
        'SELECT *'
        ' FROM tickets'
        ' ORDER BY id ASC'
    ).fetchall()  # Gets the tickets

    return tickets  # Returns the tickets


"""
USER FUNCTIONS
"""


def get_user_by_id(user_id: int) -> any:
    """ Gets a single user by user_id """
    db = get_db()  # Gets the database
    user = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE id = ?',
        (user_id,)
    ).fetchone()  # Gets the single user

    if user is None:
        abort(404, f"User {user} was not found.")

    return user  # Returns the user


def get_user_by_name(username: str) -> any:
    """ Gets a single user by username"""
    db = get_db()  # Gets the database
    user = db.execute(
        'SELECT *'
        ' FROM user'
        ' WHERE username = ?',
        (username,)
    ).fetchone()  # Gets the single user

    if user is None:
        abort(404, f"User {user} was not found.")

    return user  # Returns the user
