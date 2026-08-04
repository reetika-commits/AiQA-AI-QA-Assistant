import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

HF_MODEL = os.getenv("HF_MODEL")
HF_API_KEY = os.getenv("HF_API_KEY")