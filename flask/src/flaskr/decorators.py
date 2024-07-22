from functools import wraps
from flask import request, jsonify


def validate_json(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        return f(*args, **kwargs)

    return decorator


def validate_question(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.get_json()
        if "question" not in data or not data["question"].strip():
            return jsonify({"error": "'question' cannot be empty"}), 400
        return f(*args, **kwargs)

    return decorator


def validate_question_utf8(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.get_json()
        question = data.get("question", "")
        try:
            question.encode("utf-8")
        except UnicodeEncodeError:
            return jsonify({"error": "Invalid UTF-8 encoding"}), 400
        return f(*args, **kwargs)

    return decorator
