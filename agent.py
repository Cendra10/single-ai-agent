from dotenv import load_dotenv
from openai import OpenAI
import os

app = load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def ask_question():
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
            "role": "user",
            "content": "Halo, sebutkan 1 hal yang bisa kamu bantu"
            }
        ]
    )
    return response.choices[0].message.content
print(ask_question())