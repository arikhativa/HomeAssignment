from flask import request, jsonify
from . import Session, db
from .models import QuestionAnswer
from .dataclasses import QuestionRequest


def init_app(app):
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
