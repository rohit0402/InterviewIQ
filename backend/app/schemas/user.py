from datetime import datetime
from pydantic import BaseModel,ConfigDict,EmailStr

class UserCreate(BaseModel):
    full_name:str
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    full_name:str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class Token(BaseModel):
    access_token:str
    token_type:str="bearer"
    