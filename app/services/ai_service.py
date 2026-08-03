from app.config import settings
from app.database.sqlite_db import sqlite_procedure
import traceback
import json

def generate_testcases(requirements):
    try:
        #print("enter AI service")
        if settings.AI_PROVIDER=="ollama":
            #print("inside AI service")
            from app.services.ollama_service import generate_testcases as provider
        elif settings.AI_PROVIDER=="gimini":
            from gemini_service import generate_testcases as provider
        elif settings.AI_PROVIDER=="langchain":
            from langchain_service import generate_testcases as provider
        else:
            #log no AI provider specified
            provider = 0
  
        response= provider(requirements)
        #print("response fetched")
        #print(repr(requirements),flush=True)
        #print(json.loads(response.message.content),flush=True)
        respose_dict=json.loads(response.message.content)
        sqlite_procedure(requirements,respose_dict['testcases'])
        return response
    except Exception:
        traceback.print_exc()
        raise


