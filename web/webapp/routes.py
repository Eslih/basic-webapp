from flask import url_for, render_template, request, redirect, session, g
from flask import current_app as app
from .models import db, User
import socket
import time
import threading
from random import randint


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
        num_deleted = User.delete_users()
        session['logged_in'] = False
        return render_template('users.html', message='All users (' + str(num_deleted) + ') are deleted.')
    except Exception as e:
        return "Some very good exception handling!" + str(e)


@app.route('/users')
def users():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    try:
        data = User.query.all()
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
            data = User.query.filter_by(username=username, password=password).first()

            if data is not None:
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
            data = User.query.filter_by(username=request.form['username']).first()
            if data:
                return render_template('register.html', error='A user with this username already exits!')

            new_user = User(username=request.form['username'], password=request.form['password'])

            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            return "Some very good exception handling!" + str(e)

        return render_template('login.html')
    return render_template('register.html')


@app.route('/prime')
@app.route('/prime/<int:lower>/<int:upper>')
def prime(lower=0, upper=10000):
    if lower > 5000:
        return render_template('prime.html',
                               error='Please don\'t overload me! Lower should be less than or equal to 5000.')
    if upper > 50000:
        return render_template('prime.html', error='You exaggerator! Upper should be less than or equal to 50000.')

    p = []

    for num in range(lower, upper + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                p.append(num)

    return render_template('prime.html', primes=p)


@app.route('/cats')
def cat():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cats = [
        "https://images4.persgroep.net/rcs/zY1VwLNk62Vk5idCgHy6D5UFqFA/diocontent/72821624/_crop/0/0/1580/1444/_fitwidth/763?appId=2dc96dd3f167e919913d808324cbfeb2&quality=0.8",
        "https://www.metronieuws.nl/scale/AuZd0fUk1AT4wkjkduvV-v4dA30=/648x345/smart/filters:format(jpeg)/www.metronieuws.nl%2Fobjectstore%2Ffield%2Fimage%2Fd52b3f5401f91de0c94a92743c35f86b-1472038829.png",
        "https://images3.persgroep.net/rcs/6sClJJd-Cf4lWfMs-ENjwWYA6As/diocontent/106227942/_crop/0/0/741/555/_fitwidth/763?appId=2dc96dd3f167e919913d808324cbfeb2&quality=0.8",
        "https://i0.wp.com/vandaagindegeschiedenis.nl/wp-content/uploads-pvandag1/2013/06/garfield-560.jpg?ssl=1"
    ]

    r = randint(0, 3)

    return render_template('cat.html', cat=cats[r])


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
