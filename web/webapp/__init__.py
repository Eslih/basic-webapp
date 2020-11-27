from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SuPeR_SeCrEt_KeY'
    app.config['STATIC_FOLDER'] = '/static'
    # app.config['DEBUG'] = True
    # app.config['ENVIRONMENT'] = 'development'

    with app.app_context():
        # Imports
        from . import routes

        return app
