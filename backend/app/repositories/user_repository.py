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