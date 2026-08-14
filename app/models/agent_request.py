from pydantic import BaseModel, HttpUrl
from fastapi import File, UploadFile

class Agent_Request(BaseModel):
     web_app_URL:HttpUrl
     feature_image: UploadFile
     requirements: str