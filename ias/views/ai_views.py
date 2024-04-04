import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from dotenv import load_dotenv

from ..forms import AIForm
# from openai import OpenAI
# client = OpenAI()
#
# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Hello!"}
#   ]
# )
#
# print(completion.choices[0].message)


load_dotenv()


# Article or any paragraphs should be generated here.
@login_required(login_url='common:login')
def ai_create(request):
    API_KEY = os.getenv("OPEN_API_KEY")
    print(API_KEY)
    # if request.method == 'POST':
    #     form = AIForm(request.POST)
    #     if form.is_valid():
    #         article = form.save(commit=False)
    #         article.author = request.user  # author 속성에 로그인 계정 저장
    #         article.create_date = timezone.now()
    #         article.save()
    return redirect('ias:index')
