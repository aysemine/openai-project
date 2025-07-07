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
    data = requests.json()
    return data["current"]

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

completion = client.chat.completions.create(
    model = "gpt-4o",
    messages= messages,
    tools = tools,
)

completion.model_dump()
