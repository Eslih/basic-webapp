import requests
from flask import render_template
from ...blueprints.prime import blueprint


@blueprint.route('/')
@blueprint.route('/<int:lower>/<int:upper>')
def primes(lower=0, upper=10000):
    try:
        p = requests.get('http://api:8080/api/v1/primes/?lower={}&upper={}'.format(lower, upper))
        print(p)
        if p.status_code != 200:
            return render_template('primes.html', error=p.json()['detail'], api_headers=p.headers)
        return render_template('primes.html', primes=p.json(), api_headers=p.headers)
    except Exception as e:
        return "Some very good exception handling!" + str(e)
