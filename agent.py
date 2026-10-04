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
            "content": "Calculate 123 multiplied by 45, then the result divide by 5."
        }
    ]

    while True:
        response = client.chat.completions.create(
             model="openai/gpt-oss-20b",
             tools=tools,
             messages=messages
        )
        
        message = response.choices[0].message
        if message.tool_calls:
                tool_calls = message.tool_calls
                messages.append(message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    arguments = tool_call.function.arguments

                    args = json.loads(arguments)
                    result = calculator(**args)
                    
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        }
                    )
        else:
            print(message.content)
            break

ask_question()