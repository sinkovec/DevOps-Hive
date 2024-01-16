FROM python:3.12-slim

RUN pip install --no-cache-dir poetry~=1.7.0

WORKDIR /app

COPY pyproject.toml poetry.lock README.md ./
COPY hive ./hive

RUN poetry install

ENTRYPOINT [ "poetry", "run", "uvicorn", "hive.app:app", "--host", "0.0.0.0", "--port", "8080" ]