from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from ..models import Question

def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    question_list = Question.objects.order_by('-create_date') # -붙으면 역방향, 없으면 순방향
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}

    # render : python데이터를 템플릿에 적용해 HTML로 반환
    # 질문 목록으로 조회한 question_list 데이터를 pybo/question_list.html 파일(=Template)에 적용해 HTML을 생성한 후 리턴
    # question_list.html에서 question_list변수명으로 question_list 사용 가능
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # Question 모델에서 주어진 question_id와 일치하는 PK값을 가진 객체를 가져오거나 404에러 발생
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)