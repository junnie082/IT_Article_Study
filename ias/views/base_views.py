from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import Article


def index(request):
    page = request.GET.get('page', 1) # 페이지
    kw = request.GET.get('kw', '') # 검색어
    article_list = Article.objects.order_by('-create_date')
    if kw:
        article_list = article_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(input__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(input__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    paginator = Paginator(article_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'ias/article_list.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'ias/article_detail.html', context)