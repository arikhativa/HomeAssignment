import os
from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_url():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"


url = get_url()

engine = create_engine(url)
Session = sessionmaker(bind=engine)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=url,
        DEBUG=os.getenv("DEBUG", "False"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import routes

    @app.before_request
    def before_request():
        g.session = Session()

    @app.teardown_request
    def teardown_request(exception=None):
        session = g.pop("session", None)
        if session is not None:
            session.close()

    routes.init_app(app)

    return app
