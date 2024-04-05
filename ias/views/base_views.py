from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from ..models import AI


def ai_index(request):
    page = request.GET.get('page', 1) # 페이지
    kw = request.GET.get('kw', '') # 검색어
    ai_list = AI.objects.order_by('-create_date')
    if kw:
        ai_list = ai_list.filter(
            Q(subject__icontains=kw) | # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(ai_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'ai_list': page_obj, 'page': page, 'kw': kw}

    return render(request, 'ias/ai_list.html', context)



def ai_detail(request, ai_id):
    ai = get_object_or_404(AI, pk=ai_id)
    context = {'ai': ai}
    return render(request, 'ias/ai_detail.html', context)

