from fastapi import APIRouter,Depends
from app.schemas.user import UserResponse
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.roles import require_admin
router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me",response_model=UserResponse,status_code=200)
def get_me(current_user:User=Depends(get_current_user)):
    return current_user

@router.get("/admin")
def admin_dashboard(current_user:User=Depends(require_admin)):
    return {
        "message":"admin dashboard",
        "user":current_user.full_name
    }