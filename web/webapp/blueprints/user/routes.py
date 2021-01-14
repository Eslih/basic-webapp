import requests
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from webapp.blueprints.user import blueprint
from webapp.blueprints.user.forms import CreateAccountForm
from webapp.blueprints.util import hash_pass


# Users overview
@blueprint.route('/')
@login_required
def users():
    try:
        data = requests.get('http://api:8080/v1/users')
        return render_template('users.html', users=data.json(), api_headers=data.headers)
    except Exception as e:
        return "Some very good exception handling!" + str(e)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.home'))

    form = CreateAccountForm(request.form)

    if request.method == 'POST':
        try:
            if not form.validate_on_submit():
                return render_template('register.html', form=form)

            data = requests.post('http://api:8080/v1/register',
                                 json={'username': form.username.data, 'password': hash_pass(form.password.data),
                                       'email': form.email.data})

            if data.status_code == 400:
                return render_template('register.html', error=data.json()['error'],
                                       api_headers=data.headers, form=form)

            # HTTP Code 201 = "Created"
            if data.status_code != 201:
                return render_template('register.html',
                                       error='Something went wrong! (error code ' + str(data.status_code) + ' )',
                                       api_headers=data.headers, form=form)

            return redirect(url_for('auth_blueprint.login'))
        except Exception as e:
            print(e)
            return "Some very good exception handling!" + str(e)

    return render_template('register.html', form=form)


@blueprint.route('/delete')
@login_required
def delete_users():
    try:
        num_deleted = requests.delete('http://api:8080/v1/users/delete').json()['users_deleted']
        return render_template('users.html', message='All users (' + str(num_deleted) + ') are deleted.')
    except Exception as e:
        return "Some very good exception handling!" + str(e)
