import time
from flask import session
from flask_login import UserMixin, logout_user
import requests

from ... import login_manager


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    # https://stackoverflow.com/questions/10695093/how-to-implement-user-loader-callback-in-flask-login
    # Called on *every* single request (see Stackoverflow post)
    # This is somewhat overkill for most applications
    # Maybe a caching layer should be implemented (as suggested by Anatoly Alekseev)
    #
    # Flask login is great for persistent apps (using sessions)
    # Flask JWT is great for stateless apps

    print('============ Called user_loader')
    if time.time() - session['token_exp'] >= 0:
        return

    data = requests.get('http://api:8080/api/v1/users/' + user_id)

    if data.status_code != 200:
        return

    user = User()
    user.id = data.json()['id']
    return user


@login_manager.request_loader
def request_loader(request):
    # Can be used for "remember me" login
    # Feel free to implement something useful.
    print('============ Called request_loader')
    # username = request.form.get('username')
    #
    # if username:
    #     data = requests.get('http://api:8080/api/v1/users/username/' + username)
    # else:
    #     return None
    #
    # if data.status_code != 200:
    #     return None
    #
    # user = User()
    # user.id = data.json()['id']
    #
    # return user if user else None
