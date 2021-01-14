from flask import request, render_template, redirect, url_for, abort
from webapp.blueprints.auth import blueprint
from webapp.blueprints.auth.forms import LoginForm
from webapp.blueprints.auth.models import User
from webapp.blueprints.util import is_safe_url

import requests

from flask_login import (
    login_user,
    logout_user, login_manager, current_user
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
            data = requests.post('http://api:8080/v1/login',
                                 json={'username': form.username.data, 'password': form.password.data, 'email': ''})

            if data.status_code == 200:
                user = User()
                user.id = int(data.json()['id'])

                login_user(user)

                next = request.args.get('next')
                if not is_safe_url(next):
                    return abort(400)

                return redirect(next or url_for('home_blueprint.home'))
            else:
                return render_template('login.html',
                                       data={'username': form.username.data, 'password': form.password.data},
                                       api_headers=data.headers, form=form)

        except Exception as e:
            print(e)
            return "Some very good exception handling!"


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.login'))
