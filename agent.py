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

functions = {
    "calculator": calculator,
    "get_current_time": get_current_time
}

SYSTEM_PROMPT = "Before calling any tool, you MUST first write your plan as plain text in 1-2 sentences. Use a tool when necessary. Do not guess calculations or time. If no suitable tool is available, say so honestly."

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

REVIEWER_PROMPT = (
    "Reply with exactly 'OK' if the answer addresses every part of the question. "
    "Otherwise, reply with one sentence describing what is missing. "
    "The answer may include tool results (current time, calculations). "
    "Treat them as correct. Only check that every part of the question is answered."
    "Use the earlier conversation to resolve references like 'the result'."
)

history= []

def reflection(question, answer, history):
    messages = [
        {
            "role": "system",
            "content": REVIEWER_PROMPT
        },
        {
            "role": "user",
            "content": (
                f"Conservation history:\n{history[-2:]}\n\n"
                f"Question: {question}\nAnswer: {answer}"
            )
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages
    )

    return response.choices[0].message.content

def ask_question(feedback, is_retry=False):
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

            entry = f"Q: {user_input}\nA: {message.content}"
            history.append(entry)

            reflection_result = reflection(
                user_input,
                message.content,
                history
            )

            if reflection_result == "OK":
                print(f"[Reflection] {reflection_result}") 
                return

            else:
                print(f"[Reflection] {reflection_result}")

                if not is_retry:
                    feedback = (f"Reviewer feedback: {reflection_result} Please fix your answer.")
                    print(feedback)
                    ask_question(
                        reflection_result,
                        is_retry=True
                    )
                    print(f"[Reflection] {reflection_result}")

                break

    else:
        print("Stopped: max steps reached.")


while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    ask_question(user_input)