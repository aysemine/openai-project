import os 
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key= os.getenv("OPENAI_API_KEY"))

class CalenderEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content":"Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalenderEvent,
)

event = completion.choices[0].message.parsed
event.name
event.date
event.participants