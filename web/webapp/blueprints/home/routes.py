from flask import render_template
from ...blueprints.home import blueprint


@blueprint.route('/')
def home():
    return render_template('index.html')
