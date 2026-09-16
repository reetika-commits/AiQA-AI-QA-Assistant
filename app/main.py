from fastapi import FastAPI
from app.routes import testcase_route
from app.routes import agent_route

app = FastAPI()
# simple route that calles ai_service, creates a basic prompt and calles LLm service
#app.include_router(testcase_route.router) 

# agent route that calls orchestrator, ai_agent, 
# which then calls RAG_service, invoke graph and calls prompt_bulder according to the  
# the need_vision flag 
app.include_router(agent_route.router) 
@app.get("/")
def read_root():
    return {"application": "AiQA",
            "status": "healthy",
            "version": "1.0.0" }
