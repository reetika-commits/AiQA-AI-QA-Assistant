from langchain_ollama import ChatOllama
from app.config import settings
from app.prompts.testcase_prompt import create_prompt
import json

def generate_testcases(requirements):
    #print("inside lanchain service")
    prompt=create_prompt(requirements)
    print(prompt)
    llm=ChatOllama(model=settings.OLLAMA_MODEL)
    response=llm.invoke(prompt)
    #print(f"Response----> {response.content}")
    return json.loads(response.content)
    