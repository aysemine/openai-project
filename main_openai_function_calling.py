from openai import OpenAI
from pydantic import BaseModel, Field

import requests
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

"""basic weather api based on your location"""
def get_weather(latitude, longitude):
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

"""tools declared"""
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for provided coordinates in celsius.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "whats the weather like in Paris today?"},
]

"""chat started with openai api"""
completion = client.chat.completions.create(
    model = "gpt-4o",
    messages= messages,
    tools = tools,
)

completion.model_dump()

"""function calling"""
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )


class WeatherResponse(BaseModel):
    temperature: float = Field(
        description="The current temperature in celcius for given location."
    )
    response: str = Field(
        description="A natural language response to the user's questipn."
    )

"""converts openai response format to python base model"""
completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    response_format=WeatherResponse,
)

final_response = completion_2.choices[0].message.parsed
final_response.temperature
final_response.response