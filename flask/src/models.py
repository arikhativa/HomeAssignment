from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id = Column(Integer, primary_key=True)
    question = Column(String(), unique=False, nullable=False)
    answer = Column(String(), unique=False, nullable=False)

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        return {"id": self.id, "question": self.question, "answer": self.answer}
