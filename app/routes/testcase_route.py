from fastapi import APIRouter
from app.services.ai_service import generate_testcases
from app.models.testcase_request import RequestBody
from app.prompts.testcase_prompt import create_prompt
import traceback

router = APIRouter()

@router.post("/generate-testcases")
def generate(request_body: RequestBody):
    try:
        #print("Route reached",flush=True)
        prompt=create_prompt(request_body.requirements)
        response = generate_testcases(prompt,request_body.requirements)
        return response
    except Exception:
        traceback.print_exc()
        raise

