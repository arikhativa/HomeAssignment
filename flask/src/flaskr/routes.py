from flask import request, jsonify
from . import Session, db
from .models import QuestionAnswer
from .dataclasses import QuestionRequest
from .decorators import validate_json, validate_question, validate_question_utf8


def init_app(app):
    @app.route("/is_up", methods=["GET"])
    def is_up():
        response = {"status": 200, "message": "yes"}
        return jsonify(response), 200

    @app.route("/ask", methods=["POST"])
    @validate_json
    @validate_question
    @validate_question_utf8
    def ask():
        data = request.get_json()
        qr = QuestionRequest(**data)

        session = Session()
        qa = QuestionAnswer(question=qr.question, answer="answer")
        session.add(qa)
        session.commit()

        id = qa.id
        question = qa.question
        answer = qa.answer

        session.close()

        return jsonify({"id": id, "question": question, "answer": answer})

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

    @app.route("/qa/<int:id>", methods=["DELETE"])
    def delete_qa(id):
        session = Session()
        qa = session.query(QuestionAnswer).get(id)

        if qa is None:
            session.close()
            return handle_404_error()

        session.delete(qa)
        session.commit()
        session.close()

        return jsonify({"message": "QuestionAnswer deleted successfully"}), 200

    @app.errorhandler(404)
    def handle_404_error(error=None):
        response = {"status": 404, "message": "The requested resource was not found."}
        return jsonify(response), 404
