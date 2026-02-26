FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

# copy dependencies files from root of project
COPY pyproject.toml poetry.lock ./

# turn off creating of venv and set dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# copy common lib
COPY memo_libs /app/memo_libs

# copy user service code
COPY services/user_service /app/services/user_service

# set PYTHONPATH for well work of imports
ENV PYTHONPATH=/app

# copy entrypoint-script
COPY services/user_service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# workdir for run
WORKDIR /app/services/user_service

ENTRYPOINT ["/docker-entrypoint.sh"]

