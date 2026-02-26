FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY memo_libs /app/memo_libs

COPY services/auth_service /app/services/auth_service

ENV PYTHONPATH=/app

# copy entrypoint-script
COPY services/auth_service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

WORKDIR /app/services/auth_service

ENTRYPOINT ["/docker-entrypoint.sh"]