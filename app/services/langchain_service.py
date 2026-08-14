from langchain_ollama import ChatOllama
from app.config import settings
import json

def generate_testcases(prompt):
    #print("inside lanchain service")
    llm=ChatOllama(model=settings.OLLAMA_MODEL)
    response=llm.invoke(prompt)
    #print(f"Response----> {response.content}")
    return json.loads(response.content)
    