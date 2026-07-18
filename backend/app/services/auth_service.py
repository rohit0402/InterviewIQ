from sqlalchemy.orm import Session
from app.models.user import User    
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate,UserLogin,Token
from app.core.security import hash_password,verify_password
from app.core.jwt import create_access_token
from app.schemas.user import Token

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
        return UserRepository.create(db,user)
    
    @staticmethod
    def login(db:Session,email:str,password:str)->Token:
        user=UserRepository.get_by_email(db,email)
        if not user:
            raise ValueError("Invalid email or password")
        
        if not verify_password(password,user.hashed_password):
            raise ValueError("Invalid email or password")
        
        token=create_access_token({"sub":str(user.id),"email":user.email})
        return Token(access_token=token)