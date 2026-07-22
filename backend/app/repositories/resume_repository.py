from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.resume import Resume

class ResumeRepository:
    @staticmethod
    def get_by_user_id(db:Session,user_id:int):
        stmt=select(Resume).where(Resume.user_id==user_id)
        return db.scalar(stmt)
    
    @staticmethod
    def create(db:Session,resume:Resume):
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume
    
    @staticmethod
    def update(db:Session,resume:Resume):
        db.commit()
        db.refresh(resume)
        return resume
    
    @staticmethod
    def delete(db:Session,resume:Resume):
        db.delete(resume)
        db.commit()

    @staticmethod
    def get_by_id(db:Session,resume_id:int):
        return db.query(Resume).filter(Resume.id==resume_id).first()