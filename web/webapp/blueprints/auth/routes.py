from flask import request, render_template, redirect, url_for, abort, session
from flask_jwt_extended import decode_token

from ...blueprints.auth import blueprint
from ...blueprints.auth.forms import LoginForm
from ...blueprints.auth.models import User
from ...blueprints.util import is_safe_url

import requests

from flask_login import (
    login_user,
    logout_user, current_user
)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))

    form = LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if not form.validate_on_submit():
            return render_template('login.html', form=form)

        try:
            # Should be data and not json (endpoint expects form body)
            data = requests.post('http://api:8080/api/v1/auth/access-token',
                                 data={'username': form.email.data, 'password': form.password.data})

            if data.status_code == 200:

                user = User()
                decoded_token = decode_token(data.json()['access_token'])
                user.id = decoded_token['sub']
                session['token'] = data.json()['access_token']
                session['token_exp'] = decoded_token['exp']

                login_user(user)

                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for('home_blueprint.home'))
            else:
                return render_template('login.html',
                                       data={'username': form.email.data, 'password': form.password.data,
                                             'error': data.json()['detail']},
                                       api_headers=data.headers, form=form)

        except Exception as e:
            print(e)
            return "Some very good exception handling!"


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))
