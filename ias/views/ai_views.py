from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone

from ..function.generate import createCompletion, createSubjectContent
from ..models import AI

# Article or any paragraphs should be generated here.
@login_required(login_url='common:login')
def ai_create(request):
    topic = request.GET.get('topic', '')  # 검색어
    completion = createCompletion(topic)

    subject, content = createSubjectContent(completion.choices[0].message.content)
    # Create an instance of the AI model and populate it with the response
    ai = AI.objects.create(
        subject=subject,  # You can set the subject as needed
        content=content,
        create_date=timezone.now()
    )

    # You can print the content if needed
    # print(ai.content)

    return redirect('ias:ai_index')
