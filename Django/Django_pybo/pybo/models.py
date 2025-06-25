from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types

class Question(models.Model):
    # User 모델을 ForeignKey로 적용 (계정이 삭제되면 해당 계정이 작성한 질문 모두 삭제)
    # relation_name을 지정해 '특정 사용자.author_question,all()로 사용할 수 있음
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200) # 질문 제목
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인

    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    # Question 모델을 속성으로 가져가야 함
    # 기존 모델을 속성으로 연결하려면 ForeignKey 사용
    # CASCADE : 질문이 삭제되면 그에 달린 답변 모두 삭제
    # question 필드는 Question 모델과의 관계를 나타냄 (Question 모델의 기본키인 'id'와 견결됨)
    # 기본적으로 ForeignKey 필드를 정의할 때 외래키 필드의 이름은 '{연결된 모델의 소문자 모델명}_id' 형식으로 자동 생성됨
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

'''
BEGIN;
--
-- Create model Question
--
CREATE TABLE "pybo_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "subject" varchar(200) NOT NULL, "content" text NOT NULL, "create_date" datetime NOT NULL);
--
-- Create model Answer
--
CREATE TABLE "pybo_answer" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "create_date" datetime NOT NULL, "question_id" bigint NOT NULL REFERENCES "pybo_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "pybo_answer_question_id_e174c39f" ON "pybo_answer" ("question_id");
COMMIT;
'''