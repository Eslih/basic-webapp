FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10 as build-image

RUN apk add --no-cache g++ postgresql-dev

COPY ./requirements.txt ./

RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt



FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10 as production-image

WORKDIR '/app'

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

RUN apk add --no-cache postgresql-dev

COPY ./app ./