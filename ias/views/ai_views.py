import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from dotenv import load_dotenv

from ..forms import AIForm
from openai import OpenAI

from ..function import createSubjectContent
from ..models import AI

# client = OpenAI()



load_dotenv()


# Article or any paragraphs should be generated here.
@login_required(login_url='common:login')
def ai_create(request):
    API_KEY = os.getenv("OPEN_AI_API_KEY")
    client = OpenAI(api_key=API_KEY)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Give me one paragraph about AIs in a different way (subject, content all different). The paragraph has 4~5 lines. Title should be written as { title } content."}
        ]
    )

    subject, content = createSubjectContent(completion.choices[0].message.content)
    # Create an instance of the AI model and populate it with the response
    ai = AI.objects.create(
        subject=subject,  # You can set the subject as needed
        content=content,
        create_date=timezone.now()
    )

    # You can print the content if needed
    print(ai.content)

    return redirect('ias:ai_index')
