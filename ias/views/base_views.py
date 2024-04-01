from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Article


def index(request):
    page = request.GET.get('page', 1) # 페이지
    article_list = Article.objects.order_by('-create_date')
    paginator = Paginator(article_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'article_list': page_obj}
    return render(request, 'ias/article_list.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'ias/article_detail.html', context)