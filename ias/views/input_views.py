from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils import timezone

from ..forms import InputForm
from ..models import Article, Input


@login_required(login_url='common:login')
def input_create(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.save(commit=False)
            input.author = request.user # author 속성에 로그인 계정 저장
            input.create_date = timezone.now()
            input.article = article
            input.save()
            return redirect('{}#input_{}'.format(
                resolve_url('ias:detail', article_id=article.id), input.id
            ))
    else:
        form = InputForm()
    context = {'article': article, 'form': form}
    return render(request, 'ias/article_detail.html', context)
@login_required(login_url='common:login')
def input_modify(request, input_id):
    input = get_object_or_404(Input, pk=input_id)
    if request.user != input.author:
        messages.error(request, 'No permission to modify')
        return redirect('ias:detail', article_id=input.article.id)
    if request.method == "POST":
        form = InputForm(request.POST, instance=input)
        if form.is_valid():
            input = form.save(commit=False)
            input.modify_date = timezone.now()
            input.save()
            return redirect('{}#input_{}'.format(
                resolve_url('ias:detail', article_id=input.article.id), input.id
            ))
    else:
        form =  InputForm(instance=input)
    context = {'input': input, 'form': form}
    return render(request, 'ias/input_form.html', context)


@login_required(login_url='common:login')
def input_delete(request, input_id):
    input = get_object_or_404(Input, pk=input_id)
    if request.user != input.author:
        messages.error(request, 'No permission to delete')
    else:
        input.delete()
    return redirect('ias:detail', article_id=input.article.id)


@login_required(login_url='common:login')
def input_vote(request, input_id):
    input = get_object_or_404(Input, pk=input_id)
    if request.user == input.voter:
        messages.error(request, 'Not allowed to recommend your answer')
    else:
        input.voter.add(request.user)
    return redirect('{}#input_{}'.format(
        resolve_url('ias:detail', article_id=input.article.id), input.id
    ))