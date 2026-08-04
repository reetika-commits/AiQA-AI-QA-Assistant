from app.config import settings
from app.database.sqlite_db import sqlite_procedure
import traceback
import json

def generate_testcases(requirements):
    try:
        #print("enter AI service")
        if settings.AI_PROVIDER=="ollama":
            from app.services.ollama_service import generate_testcases as provider
        elif settings.AI_PROVIDER=="huggingface":
            print("inside AI service")
            from app.services.huggingface_service import generate_testcases as provider
        elif settings.AI_PROVIDER=="langchain":
            from langchain_service import generate_testcases as provider
        else:
            #log no AI provider specified
            provider = 0
  
        respose_dict= provider(requirements)
        print("response fetched")
        sqlite_procedure(requirements,get_dict_for_sqlite(respose_dict))
        return respose_dict
    except Exception:
        traceback.print_exc()
        raise

def get_dict_for_sqlite(respose_dict):
    if 'testcases' in respose_dict:
        testcases=respose_dict['testcases']
    else:
        testcases=respose_dict
    return testcases


