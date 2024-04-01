from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Article
from .forms import ArticleForm, InputForm
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
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.create_date = timezone.now()
            input.article = article
            input.save()
            return redirect('ias:detail', article_id=article.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'article': article, 'form': form}
    return render(request, 'ias/article_detail.html', context)


def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.create_date = timezone.now()
            article.save()
            return redirect('ias:index')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'ias/article_form.html', context)
