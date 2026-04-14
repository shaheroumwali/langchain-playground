import os
from dotenv import load_dotenv


class Config:
    MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-5-sonnet-20241022")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    SYSTEM_MESSAGE = os.getenv(
        "SYSTEM_MESSAGE", "You are a helpful Python tutor who explains concepts clearly."
    )
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))


def load_api_key():
    """Load and validate the ANTHROPIC_API_KEY from .env"""
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env file")
    return api_key
