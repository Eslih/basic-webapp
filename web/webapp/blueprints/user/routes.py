import requests
from flask import render_template, request, redirect, url_for, session
from flask_login import login_required, current_user, logout_user
from ...blueprints.user import blueprint
from ...blueprints.user.forms import CreateAccountForm


# Users overview
@blueprint.route('/')
@login_required
def users():
    try:
        data = requests.get('http://api:8080/api/v1/users', headers={'Authorization': f"Bearer {session['token']}"})
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

            data = requests.post('http://api:8080/api/v1/users/create',
                                 json={'username': form.username.data, 'password': form.password.data,
                                       'email': form.email.data})

            if data.status_code == 400:
                return render_template('register.html', error=data.json()['detail'],
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
        num_deleted = requests.delete('http://api:8080/api/v1/users/delete',
                                      headers={'Authorization': f"Bearer {session['token']}"}).json()
        logout_user()
        return render_template('users.html', message='All users (' + str(num_deleted) + ') are deleted.')
    except Exception as e:
        return "Some very good exception handling!" + str(e)
