# database.py에서 정의한 Base 클래스를 상속해야 함

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from database import Base

# 추천 (ManyToMany 관계)
question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

# 질문 모델 클래스
class Question(Base):
    __tablename__ = 'question'

    # 고유 번호 (속성)
    id = Column(Integer, primary_key=True)
    # 제목
    subject = Column(String, nullable=False)
    # 내용
    content = Column(Text, nullable=False)
    # 작성일시
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref='question_users')
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=question_voter, backref='question_voters')

# 답변 모델 클래스
class Answer(Base):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    # 답변과 질문을 연결하기 위한 속성
    # 모델을 서로 연결할 때는 ForeignKey 사용 (question 테이블의 id 컬럼이랑 연결, id 속성아님!)
    question_id = Column(Integer, ForeignKey("question.id"))
    # 답변 모델에서 질문 모델을 참조하기 위한 속성
    # answers 객체에서 연결된 질문의 제목을 answer.question.subject처럼 참조 가능
    # backref는 역참조로 ex) 한 질문에 여러 답변이 달렸다면 답변들을 참조할 수 있음
    # 질문이 a_question이라면 a_question.answer로 참조 가능
    question = relationship('Question', backref='answers')
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="answer_users")
    modify_date = Column(DateTime, nullable=True)
    voter = relationship('User', secondary=answer_voter, backref='answer_voters')

# 회원 정보 모델
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)