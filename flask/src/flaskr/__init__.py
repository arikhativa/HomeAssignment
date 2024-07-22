import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import psycopg2


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class QuestionAnswer(db.Model):
    __tablename__ = "question_answer"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), unique=False, nullable=False)
    answer = db.Column(db.String(), unique=False, nullable=False)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"id: {self.id}, question: {self.question}, answer: {self.answer}"


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.environ["SQLALCHEMY_DATABASE_URI"],
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # TODO remove hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/ask")
    def ask():
        qa = QuestionAnswer(question="What is your name?", answer="My name is Chatbot")
        db.session.add(qa)
        db.session.commit()

        return "Question added"

    @app.route("/get")
    def get():
        print(QuestionAnswer.query.all())
        return "not yet"

    db.init_app(app)

    return app
