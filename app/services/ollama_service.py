from ollama import chat
from app.config import settings
import json

def generate_testcases(prompt):
    #print("inside Ollema Service")
    response=chat(
        model=settings.OLLAMA_MODEL,
        messages=[{
            "role":"user",
            "content":prompt            
        }
        ],
        format="json"
    )
    #print(f"Char Responce---->{response}",flush=True)
    return json.loads(response.message.content)