import requests
from flask import render_template
from ...blueprints.cat import blueprint


@blueprint.route('/')
def cat():
    cat = requests.get('http://api:8080/api/v1/cats')

    return render_template('cats.html', cat=cat.json(), api_headers=cat.headers)
