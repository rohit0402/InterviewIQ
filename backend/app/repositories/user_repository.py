from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User


# db.scalar exccutes query and return either user or none
class UserRepository:
    @staticmethod
    def get_by_email(db:Session,email:str)->User | None:
        stmt=select(User).where(User.email==email)
        return db.scalar(stmt)
    
    @staticmethod
    def get_by_id(db:Session,id:int)->User | None:
        stmt=select(User).where(User.id==id)
        return db.scalar(stmt)

    @staticmethod
    def create(db:Session,user:User)->User:
        db.add(user)
        db.commit() 
        db.refresh(user)    
        return user
    
    @staticmethod
    def update_refresh_token(db: Session,user: User,refresh_token: str | None,) -> User:
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_refresh_token(db: Session, refresh_token: str) -> User | None:
        print("Searching for:", refresh_token)

        stmt = select(User).where(User.refresh_token == refresh_token)

        result = db.scalar(stmt)

        print("Result:", result)

        return result