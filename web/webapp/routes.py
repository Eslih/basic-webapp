from flask import url_for, render_template, request, redirect, session
from flask import current_app as app
from .models import db, User
import socket

@app.context_processor
def inject_hostname():
    return dict(hostname=socket.gethostname())

@app.route('/', methods=['GET'])
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


@app.route('/prime', methods=['GET'])
def prime():
    p=[]
    for num in range(0, 10000):
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
