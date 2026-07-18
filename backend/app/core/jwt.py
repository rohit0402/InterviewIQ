from datetime import datetime,timedelta,timezone
import jwt
from app.core.config import settings
from jwt.exceptions import InvalidTokenError

def create_access_token(data:dict)->str:
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)

    return encoded_jwt

def decode_access_token(token:str)->dict:
    decoded_token=jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
    return decoded_token