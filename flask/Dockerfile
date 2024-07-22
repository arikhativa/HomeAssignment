FROM python:3.9

WORKDIR /usr/src/app

COPY migrations/alembic.sh /
RUN chmod +x /alembic.sh

COPY requirements.txt .

# TODO check what mount does
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# TODO copy  alembic
COPY alembic.ini .
# COPY src .

ENTRYPOINT [ "/alembic.sh" ]

CMD flask --app flaskr run --host=0.0.0.0 --debug
