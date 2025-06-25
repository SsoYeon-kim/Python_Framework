from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.question import question_schema, question_crud
from typing import List
from starlette import status
from domain.user.user_router import get_current_user
from models import User

# 요청 url에 항상 포함되어야 하는 값
router = APIRouter(
    prefix="/api/question",
)

# question_list의 리턴값은 Question 스키마로 구성된 리스트
@router.get("/list", response_model=question_schema.QuestionList)
def question_list(db: Session = Depends(get_db),
                  page: int = 0, size: int = 10, keyword: str = ''):
    total, _question_list = question_crud.get_question_list(
        db, skip=page*size, limit=size, keyword=keyword)
    return {
        'total': total,
        'question_list': _question_list
    }

# url을 통해 얻은 question id값으로 질문 상세 내역을 조회하고 리턴 (가변적인 숫자값이기 때문에 {})
@router.get('/detail/{question_id}', response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

# 질문 등록 라우터
@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create, user=current_user)

# 질문 수정 라우터
@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def question_update(_question_update: question_schema.QuestionUpdate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    question_crud.update_question(db=db, db_question=db_question,
                                  question_update=_question_update)

# 질문 삭제 라우터
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)

# 질문 추천 라우터
@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT)
def question_vote(_question_vote: question_schema.QuestionVote,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_vote.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    question_crud.vote_question(db, db_question=db_question, db_user=current_user)