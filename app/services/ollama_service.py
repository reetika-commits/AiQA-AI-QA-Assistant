from app.models.testcase_response import ResponseBody
from ollama import chat



def generate_testcases(request_body):
    response=chat(
        model="qwen2.5:3b",
        messages=[{
            "role":"user",
            "content":request_body.requirements,
            "format":ResponseBody
        }
        ]
    )
    
    return response