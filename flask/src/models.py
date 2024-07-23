from flask import g
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql import func


Base = declarative_base()


class QuestionAnswer(Base):
    __tablename__ = "question_answer"

    id = Column(Integer, primary_key=True)
    question = Column(String(), unique=False, nullable=False)
    answer = Column(String(), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def to_dict(self):
        if self.created_at:
            return {
                "id": self.id,
                "question": self.question,
                "answer": self.answer,
                "created_at": self.created_at,
            }
        return {"id": self.id, "question": self.question, "answer": self.answer}

    def save(self):
        try:
            session = g.session
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self):
        try:
            session = g.session
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def get_by_id(cls, id):
        try:
            session = g.session
            qa = session.query(cls).get(id)
            return qa
        except Exception as e:
            raise e

    # NOTE - since this is just for testing the limit is 200
    @classmethod
    def get_all(cls, limit=200):
        try:
            session = g.session
            return session.query(cls).limit(limit).all()
        except Exception as e:
            raise e
