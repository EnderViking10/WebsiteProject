import os

from flask import Flask
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    # Create and configure the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )
    Bootstrap(app)

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import init_app
    init_app(app)

    from .pages import index
    app.register_blueprint(index.bp)
    app.add_url_rule('/', endpoint='index')

    from .pages import auth
    app.register_blueprint(auth.bp)

    from .pages import items
    app.register_blueprint(items.bp)

    from .pages import admin
    app.register_blueprint(admin.bp)

    return app
