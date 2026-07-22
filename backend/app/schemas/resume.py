from datetime import datetime
from pydantic import BaseModel,ConfigDict
from app.core.enum import ResumeStatus
class ResumeResponse(BaseModel):
    id:int
    original_filename:str
    file_size:int
    mime_type:str
    status:ResumeStatus
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)