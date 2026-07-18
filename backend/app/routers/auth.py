from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.user import UserCreate,UserResponse,UserLogin,Token
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
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