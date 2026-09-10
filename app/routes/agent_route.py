from fastapi import APIRouter, UploadFile, File, Form
from app.agents.qa_agent import agent_generate_testcases
import traceback

router = APIRouter()

#### Remove this later
# @router.post("/agent/test-features")
# def call_agent(
#     web_app_url: str = Form(...),
#     feature_image: UploadFile = File(...),
#     requirements: str = Form(...)
# ):
#     print("🔥🔥🔥 CALL_AGENT ENTERED 🔥🔥🔥", flush=True)
#     return {
#         "message": "route works",
#         "url": web_app_url,
#         "requirements": requirements
#     }

@router.post("/agent/test-features")
@router.post("/agent/test-features")
def call_agent(
    web_app_url: str = Form(...),
    feature_image: UploadFile = File(...),
    requirements: str = Form(...)
):
    try:
        response = agent_generate_testcases(
            web_app_url,
            feature_image,
            requirements
        )

        return {
            "checkpoint": "QA AGENT COMPLETED",
            "response": response
        }

    except Exception:
        return {
            "checkpoint": "QA AGENT FAILED",
            "error": traceback.format_exc()
        }