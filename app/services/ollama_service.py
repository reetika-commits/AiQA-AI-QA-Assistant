from ollama import chat
from app.prompts.testcase_prompt import create_prompt 

def generate_testcases(requirements):
    print("inside Ollema Service")
    prompt=create_prompt(requirements)
    response=chat(
        model="qwen2.5:3b",
        messages=[{
            "role":"user",
            "content":prompt            
        }
        ],
        format="json"
    )
    #print(f"Char Responce---->{response}",flush=True)
    return response