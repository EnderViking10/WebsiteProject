import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
