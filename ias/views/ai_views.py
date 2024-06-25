from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from ..function.generate import createCompletion, createText
from ..models import AI
from attendance.models import Attendance

from attendance.function.attendance import create_attendance


# Article or any paragraphs should be generated here.
@login_required(login_url='common:login')
def ai_create(request):
    topic = request.GET.get('topic', '')  # 검색어
    text = createCompletion(topic).choices[0].message.content

    paragraphs = createText(text)
    print('paragraphs[1]: ' + paragraphs[1])
    # Create an instance of the AI model and populate it with the response
    ai = AI.objects.create(
        engSubject=paragraphs[0],
        engContent=paragraphs[1].replace('-', ' '),
        korSubject=paragraphs[2],  # You can set the subject as needed
        korContent=paragraphs[3].replace('-', ' '),
        create_date=timezone.now()
    )

    create_attendance(ai)
    # print('subject: ' + str(subject) + 'content: '+ str(content))
    # You can print the content if needed
    # print(ai.content)

    return redirect('ias:ai_index')
