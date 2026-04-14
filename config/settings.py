import os
from dotenv import load_dotenv


class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    SYSTEM_MESSAGE = os.getenv(
        "SYSTEM_MESSAGE", "You are a helpful Python tutor who explains concepts clearly."
    )


def load_api_key():
    """Load and validate the GOOGLE_API_KEY from .env"""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    return api_key
