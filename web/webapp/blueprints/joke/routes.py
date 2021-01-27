import requests
from flask import render_template
from ...blueprints.joke import blueprint


@blueprint.route('/')
def joke():
    p = requests.get('http://api:8080/api/v1/jokes/')
    return render_template('joke.html', joke=p.json()['joke'], api_headers=p.headers)
