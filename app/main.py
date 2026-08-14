from fastapi import FastAPI
from app.routes import testcase_route
from app.routes import agent_route

app = FastAPI()
#app.include_router(testcase_route.router)
app.include_router(agent_route.router)
@app.get("/")
def read_root():
    return {"application": "AiQA",
            "status": "healthy",
            "version": "1.0.0" }
