from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.user import UserCreate,UserResponse,Token,RefreshTokenRequest,ChangePasswordRequest
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.auth.dependencies import get_current_user
router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserCreate,db:Session=Depends(get_db)):
    try:
        return AuthService.register(db,user)
    except ValueError as e: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
@router.post("/login",response_model=Token)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    try:
        return AuthService.login(db,form_data.username,form_data.password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
@router.post("/refresh",response_model=Token)
def refresh_token(request:RefreshTokenRequest,db:Session=Depends(get_db)):
    try:
        return AuthService.refresh_token(db,request.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
@router.post("/logout")
def logout(request:RefreshTokenRequest,db:Session=Depends(get_db)):
    try:
        return AuthService.logout(db,request.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
@router.post("/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return AuthService.change_password(
            db,
            current_user,
            request.old_password,
            request.new_password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )