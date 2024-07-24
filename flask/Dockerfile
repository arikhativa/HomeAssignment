FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

# NOTE - since this is a development image, we use volumes and not COPY
# COPY src ./src
# COPY alembic ./alembic
COPY alembic.ini .

ENTRYPOINT [ "/entrypoint.sh" ]


ENV LOG_LEVEL=info
CMD gunicorn --chdir src --bind 0.0.0.0:8000 --workers 1 --log-level=$LOG_LEVEL 'src:create_app()'