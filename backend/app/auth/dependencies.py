from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.services.auth_service import AuthService
from app.core.jwt import decode_token
from jwt.exceptions import InvalidTokenError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.core.dependencies import oauth2_scheme

def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db))->User:
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload=decode_token(token)
        user_id=payload.get("sub")

        if user_id is None:
            raise credentials_exception
    except (InvalidTokenError,ValueError):
        raise credentials_exception
    
    
    user_id = int(payload["sub"])

    user = UserRepository.get_by_id(db,user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User is not active")
    return user