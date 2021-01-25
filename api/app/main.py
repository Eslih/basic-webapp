import time
import socket
from urllib.request import Request
from fastapi import FastAPI

from . import config
from .api.api import api_router

app = FastAPI(openapi_url=f"{config.settings.API_VERSION_STR}/openapi.json")

app.include_router(api_router, prefix=config.settings.API_VERSION_STR)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    processing_time = time.time() - start_time
    response.headers["X-Process-Time"] = str("%.5fs" % processing_time)
    response.headers["X-API-Hostname"] = str(socket.gethostname())
    return response
