from dotenv import load_dotenv
from openai import OpenAI
import os
from tools import calculator, get_current_time, tools
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MAX_STEPS = 5
functions ={
     "calculator": calculator,
     "get_current_time": get_current_time
     }

def ask_question():
    messages = [
        {
            "role": "user",
            "content": "What time now ? then counting 8 multiply 7."
        }
    ]

    for step in range(MAX_STEPS):
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
                    function = functions[function_name]
                    arguments = tool_call.function.arguments
                    args = json.loads(arguments)
                    result = function(**args)
                    
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
    else:
         print("Stopped: max steps reached.") 

ask_question()