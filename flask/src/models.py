from sqlalchemy.orm import DeclarativeBase
from . import db


class Base(DeclarativeBase):
    pass


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
