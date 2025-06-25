import datetime
from pydantic import BaseModel, validator
from domain.answer.answer_schema import Answer
from typing import List, Optional
from domain.user.user_schema import User

# Question 스키마
# 질문 상세
class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: List[Answer] = []
    user: Optional[User]
    modify_date: Optional[datetime.datetime] = None
    voter: List[User] = []

    class Config:
        orm_mode = True

# 질문 목록
class QuestionList(BaseModel):
    total: int = 0
    question_list: List[Question] = []

# 질문 등록
class QuestionCreate(BaseModel):
    subject: str
    content: str

    @validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

# 질문 수정
class QuestionUpdate(QuestionCreate):
    question_id: int

# 질문 삭제
class QuestionDelete(BaseModel):
    question_id: int

# 질문 추천
class QuestionVote(BaseModel):
    question_id: int