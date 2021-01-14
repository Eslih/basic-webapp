import binascii
import hashlib
from random import randint
from typing import Optional

import requests
from fastapi import FastAPI, Response, status, Request
from fastapi_versioning import VersionedFastAPI, version
from pydantic import BaseModel

import time
import socket

from models import User, db


class Login(BaseModel):
    username: str
    password: str
    email: Optional[str] = None


app = FastAPI()


# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/
def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    password_hash = hashlib.pbkdf2_hmac('sha512',
                                        provided_password.encode('utf-8'),
                                        salt.encode('ascii'),
                                        100000)
    password_hash = binascii.hexlify(password_hash).decode('ascii')
    return password_hash == stored_password


@app.get('/', status_code=200)
@version(1)
def root():
    return {"message": "Hello World"}


@app.delete('/users/delete', status_code=200)
@version(1)
def delete_users(response: Response):
    try:
        num_deleted = User.delete_users()
        return {"users_deleted": num_deleted}
    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!" + str(e)


@app.get('/users', status_code=200)
@version(1)
def get_users(response: Response):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!" + str(e)


@app.get('/users/username/{username}', status_code=200)
@version(1)
def get_user_by_username(username, response: Response):
    try:
        data = db.query(User).filter_by(username=username).first()

        if data is not None:
            return {"id": data.json()['id']}
        else:
            response.status_code = 404
    except Exception as e:
        response.status_code = 500
        return "Some very good exception handling!"


@app.get('/users/id/{id}', status_code=200)
@version(1)
def get_user_by_id(id, response: Response):
    try:
        data = db.query(User).filter_by(id=id).first()

        if data is not None:
            return {"id": data.id}
        else:
            response.status_code = 404
    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!"


@app.post('/login', status_code=200)
@version(1)
def login(input: Login, response: Response):
    try:
        data = db.query(User).filter_by(username=input.username).first()

        if data and verify_pass(input.password, data.password):
            return {"id": data.id}
        else:
            response.status_code = 401
            return "Authentication failed"

    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!"


@app.post('/register', status_code=201)
@version(1)
def register(input: Login, response: Response):
    try:
        data = db.query(User).filter_by(username=input.username).first()
        if data:
            response.status_code = 400
            return {"error": 'A user with this username already exits!'}

        data = db.query(User).filter_by(username=input.email).first()
        if data:
            response.status_code = 400
            return {"error": 'A user with this email already exits!'}
        print(str.encode(input.password, 'utf-8'))
        new_user = User(username=input.username, email=input.email, password=str.encode(input.password, 'utf-8'))

        db.add(new_user)
        db.commit()
        return {}

    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!" + str(e)


@app.get('/primes', status_code=200)
@app.get('/primes/{lower}/{upper}', status_code=200)
@version(1)
def primes(lower: int = 0, upper: int = 10000, response: Response = None):
    try:
        if lower > 5000:
            response.status_code = 409
            return {'error': 'Please don\'t overload me! Lower should be less than or equal to 5000.'}
        if upper > 50000:
            response.status_code = 409
            return {'error': 'You exaggerator! Upper should be less than or equal to 50000.'}

        p = []

        for num in range(lower, upper + 1):
            if num > 1:
                for i in range(2, num):
                    if (num % i) == 0:
                        break
                else:
                    p.append(num)

        return p

    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!"


@app.get('/cats', status_code=200)
@version(1)
def cats(response: Response):
    try:
        cats = [
            "https://images4.persgroep.net/rcs/zY1VwLNk62Vk5idCgHy6D5UFqFA/diocontent/72821624/_crop/0/0/1580/1444/_fitwidth/763?appId=2dc96dd3f167e919913d808324cbfeb2&quality=0.8",
            "https://images3.persgroep.net/rcs/6sClJJd-Cf4lWfMs-ENjwWYA6As/diocontent/106227942/_crop/0/0/741/555/_fitwidth/763?appId=2dc96dd3f167e919913d808324cbfeb2&quality=0.8",
            "https://i0.wp.com/vandaagindegeschiedenis.nl/wp-content/uploads-pvandag1/2013/06/garfield-560.jpg?ssl=1"
        ]

        r = randint(0, 2)
        return {'cats': cats[r]}

    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!"


@app.get('/joke', status_code=200)
@version(1)
def cats(response: Response):
    try:
        joke = requests.get('https://icanhazdadjoke.com', headers={"Accept": "application/json"})
        return {'joke': joke.json()['joke']}

    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!"


app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}')


# VersionedFastAPI will only load the "title" of the original app
# Middleware should be registered or added like below :-)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time
    response.headers["X-Process-Time"] = str("%.5fs" % processing_time)
    response.headers["X-API-Hostname"] = str(socket.gethostname())
    return response
