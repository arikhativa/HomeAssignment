from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text
import requests
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class QuestionAnswer(Base):
    __tablename__ = "question_answers"
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


Base.metadata.create_all(engine)


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")

    response = requests.post(
        "https://api.openai.com/v1/answers", json={"question": question}
    )
    answer = response.json().get("answer", "Default answer")

    session = Session()
    qa = QuestionAnswer(question=question, answer=answer)
    session.add(qa)
    session.commit()
    session.close()

    return jsonify({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
