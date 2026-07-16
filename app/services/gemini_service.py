from dotenv import load_dotenv
from google import genai    
from google.genai import types
from app.models.testcase_response import ResponseBody

load_dotenv()
client = genai.Client()
# for model in client.models.list():
#     print(model.name)
def generate_testcases(request_body):
    response=client.models.generate_content(
        model="gemini-2.0-flash-lite-001",
        contents=("Generate Testcases:\n\n" + request_body.requirements),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResponseBody,
        )
    )
    print(response.text)
    return response