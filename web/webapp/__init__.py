import flask_s3
from flask import Flask
from flask_s3 import FlaskS3

s3 = FlaskS3()


def create_app():
    app = Flask(__name__)
    app.config.from_object('webapp.config.Config')

    try:
        s3.init_app(app)
        flask_s3.create_all(app, put_bucket_acl=False)
    except Exception as e:
        print('---> Something wrong with S3')
        print(e)

    with app.app_context():
        # Imports
        from . import routes

        return app
