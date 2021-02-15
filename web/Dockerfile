FROM python:3.9.1-alpine3.13 as build-image

WORKDIR '/app'

RUN apk add --no-cache linux-headers g++ git

COPY webapp/requirements.txt ./

RUN pip wheel --wheel-dir=/root/wheels -r requirements.txt



FROM python:3.9.1-alpine3.13 as production-image

WORKDIR '/app'

RUN apk add git

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN addgroup -S uwsgi && adduser -S uwsgi -G uwsgi

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

COPY ./ ./

USER uwsgi