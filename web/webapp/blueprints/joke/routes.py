import requests
from flask import render_template
from webapp.blueprints.joke import blueprint


@blueprint.route('/')
def joke():
    p = requests.get('http://api:8080/v1/joke')

    return render_template('joke.html', joke=p.json()['joke'], api_headers=p.headers)
