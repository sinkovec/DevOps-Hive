FROM python:3.12-slim@sha256:d3a32591680bdfd49da5773495730cf8afdb817e217435db66588b2c64db6d5e

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