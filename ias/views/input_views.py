from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils import timezone

from attendance.models import Attendance
# from voice.function.voice import get_speech
from ..forms import InputForm
from attendance.function.attendance import create_attendance, update_attendance
from ..function.cmpStrings import chkErrors, cmp_input_article
from ..models import Input, AI

# @login_required(login_url='common:login')
# def input_create(request, ai_id):
#     ai = get_object_or_404(AI, pk=ai_id)
#     if request.method == 'POST':
#         form = InputForm(request.POST)
#         if form.is_valid():
#             input.author = request.user
#             input.create_date = timezone.now()
#             input.ai = ai
#             input.errCheckStr = ' '.join(chkErrors(get_speech(), ai.engContent))
#             speech = get_speech()
#             input.isTheSame = cmpInputArticle(speech, ai.engContent)
#             update_attendance(input)
#             input.save()
#             return redirect('{}#input_{}'.format(
#                 resolve_url('ias:ai_detail', ai_id=ai.id), input.id
#             ))
#         else:
#             form = InputForm()
#     context = {'ai': ai, 'form': form}
#     return render(request, 'ias/ai_detail.html', context)

@login_required(login_url='common:login')
def input_modify(request, input_id):
    print('input_modify')
    input = get_object_or_404(Input, pk=input_id)
    if request.user != input.author:
        messages.error(request, 'No permission to modify')
        return redirect('ias:ai_detail', article_id=input.ai.id)
    if request.method == "POST":
        form = InputForm(request.POST, instance=input)
        if form.is_valid():
            input = form.save(commit=False)
            input.modify_date = timezone.now()
            input.errCheckedStr = ' '.join(chkErrors(input.content, input.ai.engContent))
            input.isTheSame = cmp_input_article(input.content, input.ai.engContent)
            update_attendance(input)
            input.save()
            return redirect('{}#input_{}'.format(
                resolve_url('ias:ai_detail', ai_id=input.ai.id), input.id
            ))
    else:
        form =  InputForm(instance=input)
    context = {'ai': input.ai, 'input': input, 'form': form}
    return render(request, 'ias/input_form.html', context)


@login_required(login_url='common:login')
def input_delete(request, input_id):
     input_instance = get_object_or_404(Input, pk=input_id)
     ai_id = input_instance.ai.id  # Store AI ID before deletion

     if request.user != input_instance.author:
         messages.error(request, 'No permission to delete')
     else:
         # Delete the related Attendance instance if it exists
         attendance_instance = Attendance.objects.filter(week=input_instance.ai.id, user=request.user).first()
         if attendance_instance:
             attendance_instance.delete()

         input_instance.delete()


     return redirect('ias:ai_detail', ai_id=ai_id)


@login_required(login_url='common:login')
def input_vote(request, input_id):
    input = get_object_or_404(Input, pk=input_id)
    if request.user == input.voter:
        messages.error(request, 'Not allowed to recommend your answer')
    else:
        input.voter.add(request.user)
    return redirect('{}#input_{}'.format(
        resolve_url('ias:ai_detail', ai_id=input.ai.id), input.id
    ))