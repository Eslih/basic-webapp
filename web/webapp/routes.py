import time
import socket
from datetime import datetime

from flask import g, redirect, url_for, request
from flask import current_app as app

from . import login_manager


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.context_processor
def inject_hostname():
    return dict(hostname=socket.gethostname())


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@login_manager.unauthorized_handler
def unauthorized_handler():
    print("======> " + request.full_path)
    return redirect(url_for('auth_blueprint.login', next=request.full_path))
