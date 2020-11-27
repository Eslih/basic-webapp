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


app = FastAPI()


@app.get('/', status_code=200)
@version(1)
def root():
    print("hoi")
    return {"message": "Hello World"}


@app.delete('/users/delete', status_code=200)
@version(1)
def delete_users():
    try:
        num_deleted = User.delete_users()
        return {"users_deleted": num_deleted}
    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!" + str(e)


@app.get('/users', status_code=200)
@version(1)
def get_users():
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print(e)
        response.status_code = 500
        return "Some very good exception handling!" + str(e)


@app.post('/login', status_code=200)
@version(1)
def login(input: Login, response: Response):
    try:
        data = db.query(User).filter_by(username=input.username, password=input.password).first()

        if data is not None:
            return {"status": 200}
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

        new_user = User(username=input.username, password=input.password)

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
            "https://www.metronieuws.nl/scale/AuZd0fUk1AT4wkjkduvV-v4dA30=/648x345/smart/filters:format(jpeg)/www.metronieuws.nl%2Fobjectstore%2Ffield%2Fimage%2Fd52b3f5401f91de0c94a92743c35f86b-1472038829.png",
            "https://images3.persgroep.net/rcs/6sClJJd-Cf4lWfMs-ENjwWYA6As/diocontent/106227942/_crop/0/0/741/555/_fitwidth/763?appId=2dc96dd3f167e919913d808324cbfeb2&quality=0.8",
            "https://i0.wp.com/vandaagindegeschiedenis.nl/wp-content/uploads-pvandag1/2013/06/garfield-560.jpg?ssl=1"
        ]

        r = randint(0, 3)
        return {'cats': cats[r]}

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