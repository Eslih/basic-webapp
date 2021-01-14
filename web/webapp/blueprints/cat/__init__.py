from flask import Blueprint

blueprint = Blueprint(
    'cat_blueprint',
    __name__,
    url_prefix='/cat',
    template_folder='templates'
)
