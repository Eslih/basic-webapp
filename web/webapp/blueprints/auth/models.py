from flask_login import UserMixin
import requests

from webapp import login_manager


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(user_id):
    # https://stackoverflow.com/questions/10695093/how-to-implement-user-loader-callback-in-flask-login
    # Called on *every* single request (see Stackoverflow post)
    # This is somewhat overkill for most applications
    # Maybe a caching layer should be implemented (as suggested by Anatoly Alekseev)
    print('============ Called user_loader')
    data = requests.get('http://api:8080/v1/users/id/' + user_id)

    if data.status_code != 200:
        return

    user = User()
    user.id = data.json()['id']
    return user


@login_manager.request_loader
def request_loader(request):
    print('============ Called request_loader')
    username = request.form.get('username')

    if username:
        data = requests.get('http://api:8080/v1/users/username/' + username)
    else:
        return None

    if data.status_code != 200:
        return None

    user = User()
    user.id = data.json()['id']

    return user if user else None
