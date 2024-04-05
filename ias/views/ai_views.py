from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from ..function.generate import createCompletion, createText
from ..models import AI

# Article or any paragraphs should be generated here.
@login_required(login_url='common:login')
def ai_create(request):
    topic = request.GET.get('topic', '')  # 검색어
    text = createCompletion(topic).choices[0].message.content

    print('text: ' + text)
    paragraphs = createText(text)
    # Create an instance of the AI model and populate it with the response
    ai = AI.objects.create(
        engSubject=paragraphs[0],
        engContent=paragraphs[1],
        korSubject=paragraphs[2],  # You can set the subject as needed
        korContent=paragraphs[3],
        create_date=timezone.now()
    )

    # print('subject: ' + str(subject) + 'content: '+ str(content))
    # You can print the content if needed
    # print(ai.content)

    return redirect('ias:ai_index')
