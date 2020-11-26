from flask import url_for, render_template, request, redirect, session, g
from flask import current_app as app

import socket
import time
import requests


@app.context_processor
def inject_hostname():
    return dict(hostname=socket.gethostname())


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/users/delete')
def delete_users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        num_deleted = requests.delete('http://api:8080/v1/users/delete').json()['users_deleted']
        session['logged_in'] = False
        return render_template('users.html', message='All users (' + str(num_deleted) + ') are deleted.')
    except Exception as e:
        return "Some very good exception handling!" + str(e)


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        data = requests.get('http://api:8080/v1/users').json()
        return render_template('users.html', users=data)
    except Exception as e:
        return "Some very good exception handling!" + str(e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = requests.post('http://api:8080/v1/login', json={'username': username, 'password': password})

            if data.status_code == 200:
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template('index.html', data={'username': username, 'password': password})

        except Exception as e:
            return "Some very good exception handling!"


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            data = requests.post('http://api:8080/v1/register', json={'username': username, 'password': password})
            if data.status_code != 201:
                return render_template('register.html', error='A user with this username already exits!')

        except Exception as e:
            return "Some very good exception handling!" + str(e)

        return render_template('login.html')
    return render_template('register.html')


@app.route('/primes')
@app.route('/primes/<int:lower>/<int:upper>')
def prime(lower=0, upper=10000):
    p = requests.get('http://api:8080/v1/primes/{}/{}'.format(lower, upper))
    if p.status_code != 200:
        return render_template('primes.html', error=p.json()['error'])
    return render_template('primes.html', primes=p.json())


@app.route('/cats')
def cat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    p = requests.get('http://api:8080/v1/cats').json()['cats']

    return render_template('cats.html', cat=p)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
