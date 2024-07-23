from flask import request, jsonify, g
from . import Session
from .models import QuestionAnswer
from .dataclasses import QuestionRequest
from .decorators import validate_json, validate_question
from .service_openai import call_openai


def init_app(app):
    @app.route("/is_up", methods=["GET"])
    def is_up():
        response = {"status": 200, "message": "yes"}
        return jsonify(response), 200

    @app.route("/ask", methods=["POST"])
    @validate_json
    @validate_question
    def ask():
        data = request.get_json()
        qr = QuestionRequest(**data)

        answer, stt = call_openai(qr.question)
        if not stt:
            app.logger.error(answer)
            return jsonify({"message": "An error occurred"}), 500

        session = g.session
        qa = QuestionAnswer(question=qr.question, answer=answer)
        session.add(qa)
        session.commit()

        id = qa.id
        question = qa.question
        answer = qa.answer

        return jsonify({"id": id, "question": question, "answer": answer})

    @app.route("/qa/<int:id>", methods=["GET"])
    def qa(id):
        session = g.session
        qa = session.query(QuestionAnswer).get(id)

        if qa is None:
            return handle_404_error()

        return jsonify({"id": qa.id, "question": qa.question, "answer": qa.answer})

    @app.route("/qas", methods=["GET"])
    def qas():
        session = g.session
        # NOTE - since this is just for testing the limit is 200
        questions = session.query(QuestionAnswer).limit(200).all()

        result = [
            {"id": qa.id, "question": qa.question, "answer": qa.answer}
            for qa in questions
        ]

        return jsonify(result)

    @app.route("/qa/<int:id>", methods=["DELETE"])
    def delete_qa(id):
        session = g.session
        qa = session.query(QuestionAnswer).get(id)

        if qa is None:
            return handle_404_error()

        session.delete(qa)
        session.commit()

        return jsonify({"message": "QuestionAnswer deleted successfully"}), 200

    @app.errorhandler(404)
    def handle_404_error(error=None):
        response = {"status": 404, "message": "The requested resource was not found."}
        return jsonify(response), 404
