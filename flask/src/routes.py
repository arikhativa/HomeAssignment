from flask import request, jsonify, g
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
            return handle_500_error(e)

        qa = QuestionAnswer(question=qr.question, answer=answer)
        try:
            qa.save()
        except Exception as e:
            return handle_500_error(e)

        id = qa.id
        question = qa.question
        answer = qa.answer

        return jsonify({"id": id, "question": question, "answer": answer})

    @app.route("/qa/<int:id>", methods=["GET"])
    def qa(id):
        try:
            qa = QuestionAnswer.get_by_id(id)
        except Exception as e:
            return handle_500_error(e)

        if qa is None:
            return handle_404_error()

        return jsonify({"id": qa.id, "question": qa.question, "answer": qa.answer})

    @app.route("/qas", methods=["GET"])
    def qas():
        try:
            qas = QuestionAnswer.get_all(200)
        except Exception as e:
            return handle_500_error(e)

        result = [
            {"id": qa.id, "question": qa.question, "answer": qa.answer} for qa in qas
        ]

        return jsonify(result)

    @app.route("/qa/<int:id>", methods=["DELETE"])
    def delete_qa(id):
        qa = QuestionAnswer.get_by_id(id)

        if qa is None:
            return handle_404_error()

        try:
            qa.delete()
        except Exception as e:
            return handle_500_error(e)

        return jsonify({"message": "QuestionAnswer deleted successfully"}), 200

    @app.errorhandler(404)
    def handle_404_error(error=None):
        response = {"status": 404, "message": "The requested resource was not found."}
        return jsonify(response), 404

    @app.errorhandler(500)
    def handle_500_error(error=None):
        app.logger.error(error)
        response = {"status": 500, "message": "Internal Error"}
        return jsonify(response), 500
