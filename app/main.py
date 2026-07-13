from fastapi import FastAPI
from pydantic import BaseModel
from google import genai    
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()
app = FastAPI()

@app.get("/")
def read_root():
    return {"application": "AiQA",
            "status": "healthy",
            "version": "1.0.0" }

class RequestBody(BaseModel):
    requirements: str

class ResponseBody(BaseModel):
    features: str #positive, negative, neutral
    test_case: int # 1 (very bad) to 5 (very good)

@app.post("/generate-testcases")
def generate_testcases_sentiment(request_body: RequestBody):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=("Generate Testcases:\n\n" + request_body.requirements),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ResponseBody,
        )
    )
    print(response.text)
    return response.text