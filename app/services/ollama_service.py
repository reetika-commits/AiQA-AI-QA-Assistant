from ollama import chat
from app.config import settings
from app.prompts.testcase_prompt import create_prompt 
import json

def generate_testcases(requirements):
    #print("inside Ollema Service")
    prompt=create_prompt(requirements)
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