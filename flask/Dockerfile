FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt .

# TODO check what mount does
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY src .

CMD flask --app flaskr run --host=0.0.0.0 --debug
