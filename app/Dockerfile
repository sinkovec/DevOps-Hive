FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY hive ./hive

RUN poetry install

ENTRYPOINT [ "poetry", "run", "start" ]