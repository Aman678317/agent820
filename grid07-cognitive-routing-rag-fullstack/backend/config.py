import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()

def is_mock():
    return LLM_PROVIDER != "openai" or not OPENAI_API_KEY
