from django.shortcuts import render
from .models import Article
# Create your views here.

def index(request):
    article_list = Article.objects.order_by('-create_date')
    context = {'article_list': article_list}
    print("article_list: " + str(article_list))
    return render(request, 'ias/article_list.html', context)

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    context = {'article': article}
    return render(request, 'ias/article_detail.html', context)