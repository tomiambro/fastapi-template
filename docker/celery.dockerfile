FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin/:${PATH}"

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi --extras monitoring

