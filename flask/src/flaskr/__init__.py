import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dataclasses import dataclass


@dataclass
class QuestionRequest:
    question: str


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

    def to_dict(self):
        return {"id": self.id, "question": self.question, "answer": self.answer}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.environ["SQLALCHEMY_DATABASE_URI"],
    )

    engine = create_engine(os.environ["SQLALCHEMY_DATABASE_URI"])
    Session = sessionmaker(bind=engine)

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

    @app.route("/ask", methods=["POST"])
    def ask():
        data = request.get_json()

        question_request = QuestionRequest(**data)

        session = Session()
        qa = QuestionAnswer(question=question_request.question, answer="answer")
        session.add(qa)
        session.commit()
        session.close()

        return "Question added"

    @app.route("/qa/<int:id>", methods=["GET"])
    def qa(id):
        session = Session()
        qa = session.query(QuestionAnswer).get(id)
        session.close()

        if qa is None:
            return handle_404_error()

        return jsonify({"id": qa.id, "question": qa.question, "answer": qa.answer})

    @app.route("/qas", methods=["GET"])
    def qas():
        session = Session()
        questions = session.query(QuestionAnswer).all()
        session.close()

        result = [
            {"id": qa.id, "question": qa.question, "answer": qa.answer}
            for qa in questions
        ]

        return jsonify(result)

    @app.errorhandler(404)
    def handle_404_error(error=None):
        response = {"status": 404, "message": "The requested resource was not found."}
        return jsonify(response), 404

    db.init_app(app)

    return app
