from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Article
# Create your views here.

def index(request):
    article_list = Article.objects.order_by('-create_date')
    context = {'article_list': article_list}
    return render(request, 'ias/article_list.html', context)

def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {'article': article}
    return render(request, 'ias/article_detail.html', context)

def input_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    article.input_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('ias:detail', article_id=article.id)