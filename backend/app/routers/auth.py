from fastapi import APIRouter,Depends,HTTPException,status,Response,Request
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.user import UserCreate,UserResponse,Token,RefreshTokenRequest,ChangePasswordRequest,UserLogin
from app.services.password_reset_service import PasswordResetService
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.schemas.auth import ForgotPasswordRequest,ResetPasswordRequest
from pydantic import EmailStr
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
    
@router.post("/login", response_model=Token)
def login(
    response: Response,
    request: UserLogin,
    db: Session = Depends(get_db),
):
    try:
        token = AuthService.login(
            db,
            request.email,
            request.password,
        )

        response.set_cookie(
            key="refresh_token",
            value=token.refresh_token,
            httponly=True,
            secure=False,          # True in production (HTTPS)
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
        )

        return {
            "access_token": token.access_token,
        }

    except ValueError as e:
        raise HTTPException(400, str(e))
    
@router.post("/refresh", response_model=Token)
def refresh_token(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token is None:
        raise HTTPException(401, "Refresh token missing")

    try:
        token = AuthService.refresh_token(
            db,
            refresh_token,
        )

        return {
            "access_token": token.access_token,
        }

    except ValueError as e:
        raise HTTPException(401, str(e))
    
@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        AuthService.logout(db, refresh_token)

    response.delete_cookie("refresh_token")

    return {
        "message": "Logged out successfully"
    }
    
@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return AuthService.forgot_password(
        db,
        request.email,
    )


@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return AuthService.reset_password(
        db,
        request.token,
        request.password,
    )

@router.get("/verify-email")
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):
    AuthService.verify_email(
        db,
        token,
    )

    return {
        "message": "Email verified successfully."
    }

@router.post("/resend-verification")
def resend_verification(
    email: EmailStr,
    db: Session = Depends(get_db),
):
    return AuthService.resend_verification(
        db,
        email,
    )



