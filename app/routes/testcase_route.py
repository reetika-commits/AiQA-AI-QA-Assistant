from fastapi import APIRouter
from app.services.ai_service import generate_testcases
from app.models.testcase_request import RequestBody

router = APIRouter()

@router.post("/generate-testcases")
def generate(request_body: RequestBody):
    response = generate_testcases(request_body)
    return response

