import requests
from flask import render_template
from webapp.blueprints.cat import blueprint


@blueprint.route('/')
def cat():
    p = requests.get('http://api:8080/api/v1/cats')

    return render_template('cats.html', cat=p.json()['cats'], api_headers=p.headers)
