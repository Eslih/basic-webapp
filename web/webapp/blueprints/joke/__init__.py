from flask import Blueprint

blueprint = Blueprint(
    'joke_blueprint',
    __name__,
    url_prefix='/joke',
    template_folder='templates'
)
