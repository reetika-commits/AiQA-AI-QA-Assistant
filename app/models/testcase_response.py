from pydantic import BaseModel

class ResponseBody(BaseModel):
    features: str 
    test_case: int 
