import os
import re

from dotenv import load_dotenv
import openai
from openai import OpenAI

load_dotenv()
API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=API_KEY)

def createCompletion(topic):
    print('topic: ' + str(topic))
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user",
             "content": "Give me one paragraph about %s in a different way (subject, content all different) in both English and Korean. " \
                        "The title should be wrapped in {}, and content should be wrapped in [] for both English and Korean paragraphs." \
                        "First paragraph is { title } content" \
                        "Second paragraph is { 제목 } 내용 and should be wrapped in the [ ].  " \
                        "Each paragraph has 7 lines. " \
                        % topic}
        ]
    )

    return completion
def createText(text):
    paragraphs = re.split(r'[\{\}\[\]]', text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return paragraphs




