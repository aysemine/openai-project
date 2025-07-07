import os
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Add two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

def calculator(a: float, b: float) -> str:
    print("Tool has been called.")

    return f"The result of {a} + {b} is {a + b}"

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "quit":
        break

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}],
        tools=tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = calculator(**args)

            messages = [
                {"role": "user", "content": user_input},
                msg,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            ]

            final = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            print("Assistant:", final.choices[0].message.content)
    else:
        print("Assistant:", msg.content)
