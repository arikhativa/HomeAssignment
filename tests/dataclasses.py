from dataclasses import dataclass


@dataclass
class QuestionAnswerData:
    id: int
    question: str
    answer: str
