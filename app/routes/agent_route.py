from fastapi import APIRouter, UploadFile, File, Form
from app.agents.qa_agent import agent_generate_testcases
import traceback

router = APIRouter()


@router.post("/agent/test-features")
def call_agent(
    web_app_url: str = Form(...),
    feature_image: UploadFile = File(...),
    requirements: str = Form(...)
):
    try:
        print("Route reached", flush=True)

        response = agent_generate_testcases(
            web_app_url,
            feature_image,
            requirements
        )

        return response

    except Exception:
        traceback.print_exc()
        raise