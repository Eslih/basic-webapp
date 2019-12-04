from flask import url_for, render_template, request, redirect, session, g
from flask import current_app as app
from .models import db, User
import socket
import time

@app.context_processor
def inject_hostname():
    return dict(hostname=socket.gethostname())

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        return render_template('index.html')


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
        new_user = User(username=request.form['username'], password=request.form['password'])

        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')


@app.route('/prime')
@app.route('/prime/<int:lower>/<int:upper>')
def prime(lower=0, upper=10000):
    if lower > 5000:
        return render_template('prime.html', error='Please don\'t overload me! Lower should be less than or equal to 5000.')
    if upper > 50000:
        return render_template('prime.html', error='You exaggerator! Upper should be less than or equal to 50000.')

    p=[]
    for num in range(lower, upper+1):
       if num > 1:
           for i in range(2, num):
               if (num % i) == 0:
                   break
           else:
               p.append(num)

    return render_template('prime.html', primes=p)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)
