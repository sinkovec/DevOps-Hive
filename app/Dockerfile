FROM python:3.13-slim@sha256:751d8bece269ba9e672b3f2226050e7e6fb3f3da3408b5dcb5d415a054fcb061

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir poetry~=1.7.0

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY hive ./hive
COPY config ./config

RUN poetry install --without=dev

USER nobody

ENTRYPOINT [ "poetry", "run", "uvicorn", "hive.app:app", "--host", "0.0.0.0", "--port", "8080" ]