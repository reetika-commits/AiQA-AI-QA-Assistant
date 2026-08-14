from huggingface_hub import InferenceClient
from app.config import settings
import json

client =InferenceClient(api_key=settings.HF_API_KEY)

def generate_testcases(prompt):
    #print("inside huggingface Service")
    response=client.chat_completion(
        model=settings.HF_MODEL,
        messages=[{
            "role":"user",
            "content":prompt            
        }
        ],
    )
    #print(settings.HF_MODEL)
    #print(f"Char Responce---->{response}",flush=True)
    return json.loads(response.choices[0].message.content)