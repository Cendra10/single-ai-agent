from dotenv import load_dotenv
from openai import OpenAI
import os
from tools import calculator, tools
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def ask_question():
    messages = [
        {
            "role": "user",
            "content": "How much 123 multiply 45?"
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        tools=tools,
        messages=messages
    )

    message = response.choices[0].message

    if message.tool_calls:

        tool_calls = message.tool_calls
        tool_call = tool_calls[0]

        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        args = json.loads(arguments)
        result = calculator(**args)

        messages.append(message)
        
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            }
        )

        response2 = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            tools=tools,
            messages=messages
        )

        print(response2.choices[0].message.content)
    else:
        print(message.content)

ask_question()