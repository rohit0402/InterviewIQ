from fastapi import Depends,HTTPException,status
from app.auth.dependencies import get_current_user
from app.core.enum import UserRole
from app.models.user import User

def require_admin(current_user:User=Depends(get_current_user))->User:
    if current_user.role!=UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized")
    return current_user

def require_company(current_user:User=Depends(get_current_user))->User:
    if current_user.role!=UserRole.COMPANY.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized")
    return current_user

def require_candidate(current_user:User=Depends(get_current_user))->User:
    if current_user.role!=UserRole.CANDIDATE.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorized")
    return current_user 