from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'super secret key'
    # app.config['DEBUG'] = True
    # app.config['ENVIRONMENT'] = 'development'

    with app.app_context():
        # Imports
        from . import routes

        return app
