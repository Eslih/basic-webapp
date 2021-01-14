from glob import glob

import flask_s3
from flask import Flask
from flask_s3 import FlaskS3
from importlib import import_module
from flask_login import LoginManager

s3 = FlaskS3()
login_manager = LoginManager()


def register_blueprints(app):
    for module_name in glob("webapp/blueprints/*/"):
        module = import_module(module_name.replace('/', '.') + 'routes')
        app.register_blueprint(module.blueprint)


def register_extensions(app):
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    aws_s3(app)


def aws_s3(app):
    try:
        s3.init_app(app)
        flask_s3.create_all(app, put_bucket_acl=False)
    except Exception as e:
        print('---> Something wrong with S3')
        print(e)


def create_app():
    app = Flask(__name__)
    app.config.from_object('webapp.config.Config')
    register_blueprints(app)
    register_extensions(app)

    with app.app_context():
        # Imports
        from . import routes

        return app
