from fastapi import APIRouter
from app.services.ai_service import generate_testcases
from app.models.testcase_request import RequestBody
import traceback

router = APIRouter()

@router.post("/generate-testcases")
def generate(request_body: RequestBody):
    try:
        #print("Route reached",flush=True)
        response = generate_testcases(request_body.requirements)
        return response
    except Exception:
        traceback.print_exc()
        raise

# @router.post("/generate-testcases")
# def generate(request_body: RequestBody):
#     print("Route reached", flush=True)
#     return {"status": "ok"}