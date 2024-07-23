FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

# TODO check what mount does
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y postgresql-client

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .

ENTRYPOINT [ "/entrypoint.sh" ]

CMD flask --app src run --host=0.0.0.0
