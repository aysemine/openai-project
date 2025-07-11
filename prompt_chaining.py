from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o"

class EventExtraction(BaseModel):
    description: str = Field(description="Raw description of the events")
    is_calender_event: bool = Field(description="Whether this text describes a calender event")
    confidence_score: float = Field(description="Confidence score between 0 and 1")

class EventDetails(BaseModel):
    name: str = Field(description="Name of the event")
    date: str = Field(description="date of the event use ISO 8601 format")
    duration_minutes: int = Field(description="expected duration in minutes")
    participants: list[str] = Field(description="list of participants")

class EventConfirmation(BaseModel):
    confirmation_message: str = Field(description="natural language confirmation message")
    calender_link: Optional[str] = Field(description="generated calender link if applicable")

def extract_event_info(user_input: str) -> EventExtraction:
    logger.info("Starting event extraction analysis")
    logger.debut(f"Input text: {user_input}")

    today = datetime.now()
    date_context = f"today is {today.strftime('%A, %B %d, %Y')}."

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": f"{date_context} Analyze if the text describes a calender evet"},
            {"role": "user", "content": user_input},
        ],
        response_format=EventExtraction,
    )
    result = completion.choices[0].message.parsed
    logger.info(
        f"Extraction complete - Is calender event: {result.is_calender_event}, confidence: {result.confidence_score:.2f}"
    )
    return result

def parse_event_details(description: str) -> EventDetails:
    logger.info("start event details parsing")

    today= datetime.now()
    date_context = f"today is {today.strftime('%A, %B %d, %Y')}."

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": f"{date_context} extract detailed event information when dates reference 'next tuesday' or similar relative dates use this current date as reference"},
            {"role": "user", "content": description},
        ],
        response_format=EventDetails,
    )
    result = completion.choices[0].message.parsed
    logger.info(f"parsed event details - Name: {result.name}, Date: {result.date}, Duration: {result.duration_minutes}min")
    logger.debug(f"Participatns: {', '.join(result.participants)}")
    return result

def generate_confirmation(event_details: EventDetails, name: str) -> EventConfirmation:
    logger.info("Generating confirmation message")

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "generate a natural confimation message for event. sign og with your name; {name}"},
            {"role": "user", "content": str(event_details.model_dump())},
        ],
        response_format=EventConfirmation,
    )
    result = completion.choices[0].message.parsed
    logger.info("confimation message generated succesfully")
    return result

def process_calender_request(user_input: str) -> Optional[EventConfirmation]:
    logger.info("Processing calender requests")
    logger.debug(f"Raw input: {user_input}")

    initial_extraction = extract_event_info(user_input)

    if (
        not initial_extraction.is_calender_event or
        initial_extraction.confidence_score < 0.7
    ):
        logger.warning(f"Gate check failed - is_calender_event: {initial_extraction.is_calender_event}, confidence: {initial_extraction.confidence_score:.2f}")
        return None
    
    logger.info("Gate check passed, proceeding with event processing")

    event_details = parse_event_details(initial_extraction.description)
    confirmation = generate_confirmation(event_details, name="nozaki")

    logger.info("Calender request processing completed succesfully")
    return confirmation

"""test inputs"""
user_input = "Let's schedule a 1h team meeting next Tuesday at 2pm with Alice and Bob to discuss the project roadmap."

result = process_calender_request(user_input)
if result:
    print(f"Confirmation: {result.confirmation_message}")
    if result.calendar_link:
        print(f"Calendar Link: {result.calendar_link}")
else:
    print("This doesn't appear to be a calendar event request.")


user_input = "Can you send an email to Alice and Bob to discuss the project roadmap?"

result = process_calender_request(user_input)
if result:
    print(f"Confirmation: {result.confirmation_message}")
    if result.calendar_link:
        print(f"Calendar Link: {result.calendar_link}")
else:
    print("This doesn't appear to be a calendar event request.")


