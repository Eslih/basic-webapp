from flask import Blueprint

blueprint = Blueprint(
    'prime_blueprint',
    __name__,
    url_prefix='/prime',
    template_folder='templates'
)
