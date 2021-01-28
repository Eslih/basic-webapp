FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10 as build-image

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.4 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR '/app'

RUN apk add --no-cache g++ postgresql-dev curl libffi-dev

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry export --without-hashes -f requirements.txt > requirements.txt \
        && pip wheel --wheel-dir=/root/wheels -r requirements.txt



FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10 as production-image

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR '/app'

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

RUN apk add --no-cache postgresql-dev

COPY ./ ./

