import os

from dotenv import load_dotenv
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
             "content": "Give me one paragraph about %s in a different way (subject, content all different). The paragraph has 4~5 lines. Title should be written as { title } content." % topic}
        ]
    )
    return completion
def createSubjectContent(string):
    subject, content = "", ""
    for i, c in enumerate(string):
        if c == '{':
            continue
        elif c == '}':
            content = string[i+1:]
            break
        else:
            subject += c

    # print("subject:", subject, "content:", content)
    return subject, content




