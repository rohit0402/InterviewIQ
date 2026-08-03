from sqlalchemy.orm import Session
from app.models.user import User    
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate,TokenPair
from app.core.security import hash_password,verify_password
from app.core.jwt import create_access_token,create_refresh_token,decode_token
from app.services.email_verification_service import EmailVerificationService
from app.services.password_reset_service import PasswordResetService
from app.tasks.email_tasks import send_verification_email_task
class AuthService:
    @staticmethod
    def register(db:Session,user:UserCreate)->User:
        existing_user=UserRepository.get_by_email(db,user.email)
        if existing_user:
            raise ValueError("User already exists")
        user=User(
            full_name=user.full_name,
            email=user.email,
            hashed_password=hash_password(user.password)
        )
        user = UserRepository.create(db, user)
        token = EmailVerificationService.create_token(
            db,
            user,
        )

        send_verification_email_task.delay(user.email,token,)
        return user

    @staticmethod
    def verify_email(
        db,
        token: str,
    ):
        return EmailVerificationService.verify_token(
            db,
            token,
        )
    
    @staticmethod
    def login(db:Session,email:str,password:str)->TokenPair:
        user=UserRepository.get_by_email(db,email)
        if not user:
            raise ValueError("Invalid email or password")
        if not user.is_verified:
            raise ValueError(
                "Please verify your email before logging in."
            )

        
        if not verify_password(password,user.hashed_password):
            raise ValueError("Invalid email or password")
        
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        UserRepository.update_refresh_token(
            db,
            user,
            refresh_token,
        )

        return TokenPair(
    access_token=access_token,
    refresh_token=refresh_token,
)
    
    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> TokenPair:
        print("=" * 60)
        print("COOKIE TOKEN:", refresh_token)

        user = UserRepository.get_by_refresh_token(db, refresh_token)

        print("USER FOUND:", user)

        if user is None:
            raise ValueError("Invalid refresh token")

        try:
            payload = decode_token(refresh_token)
            print("PAYLOAD:", payload)
        except Exception as e:
            print("JWT ERROR:", e)
            raise ValueError("Invalid or expired refresh token")

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    @staticmethod
    def logout(db: Session, refresh_token: str):
        user = UserRepository.get_by_refresh_token(db,refresh_token,)
        if user is None:
            raise ValueError("Invalid refresh token")

        UserRepository.update_refresh_token(db,user,None,)

        return {
            "message": "Logged out successfully"
        }
    
    @staticmethod
    def change_password(
        db: Session,
        current_user: User,
        old_password: str,
        new_password: str,
    ):
        if not verify_password(
            old_password,
            current_user.hashed_password,
        ):
            raise ValueError("Old password is incorrect")

        current_user.hashed_password = hash_password(
            new_password
        )

        db.commit()
        db.refresh(current_user)

        return {
            "message": "Password changed successfully"
        }

    @staticmethod
    def forgot_password(
        db: Session,
        email: str,
    ):
        return PasswordResetService.forgot_password(
            db,
            email,
        )


    @staticmethod
    def reset_password(
        db: Session,
        token: str,
        new_password: str,
    ):
        return PasswordResetService.reset_password(
            db,
            token,
            new_password,
        )