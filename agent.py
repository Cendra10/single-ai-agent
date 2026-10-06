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

SYSTEM_PROMPT = "Before calling any tool, you MUST first write your plan as plain text in 1-2 sentences. Use a tool when necessary. do not guess calculations or time. If no suitable tool is available, say so honestly."
    
messages = [
     {
          "role": "system",
          "content": SYSTEM_PROMPT
     }
]


def ask_question(user_input):
    messages.append(
         {
              "role": "user",
              "content": user_input
         }
    )

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

                if message.content:
                     print(message.content)

                for tool_call in tool_calls:
                        function_name = tool_call.function.name

                        if function_name not in functions:
                              result = f"Error: tool '{function_name}' is not available."
                        else:
                            try:
                                function = functions[function_name]
                                arguments = tool_call.function.arguments
                                args = json.loads(arguments)
                                result = function(**args)
                            except Exception as e:
                                 result = f"Error: {e}"
                        messages.append(
                             {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": str(result)
                            }
                        )
                         
        else:
            print(message.content)
            messages.append(message)
            break
    else:
         print("Stopped: max steps reached.") 

while True:
     user_input = input("You: ")

     if user_input.lower() == "exit":
          break
     ask_question(user_input)