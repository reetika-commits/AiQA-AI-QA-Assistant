from app.config import settings

def generate_testcases(request_body):
    if settings.AI_PROVIDER=="ollama":
        from app.services.ollama_service import generate_testcases as provider
    elif settings.AI_PROVIDER=="gimini":
        from gemini_service import generate_testcases as provider
    elif settings.AI_PROVIDER=="langchain":
        from langchain_service import generate_testcases as provider
    else:
        #log no AI provider specified
        provider = 0
    return provider(request_body)
