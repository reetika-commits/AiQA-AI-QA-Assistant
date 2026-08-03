from pydantic import BaseModel

class ResponseBody(BaseModel):
        Test_Case_ID: int
        Title: str
        Preconditions: str
        Test_Steps: str
        Expected_Result : str
        Priority : str
