from sqlalchemy.orm import Session
from app.models.resume_analysis import ResumeAnalysis

class ResumeAnalysisRepository:

    @staticmethod
    def get_by_resume_id(db:Session,resume_id:int):
        return db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id==resume_id).first()
    

    @staticmethod
    def create(db:Session,resume_analysis:ResumeAnalysis):
        db.add(resume_analysis)
        db.commit()
        db.refresh(resume_analysis)
        return resume_analysis
    
    @staticmethod
    def update(db:Session,resume_analysis:ResumeAnalysis):
        db.commit()
        db.refresh(resume_analysis)
        return resume_analysis
    
    @staticmethod
    def get_by_id(db:Session,analysis_id:int):
        return (db.query(ResumeAnalysis).filter(ResumeAnalysis.id==analysis_id).first())
    
    @staticmethod
    def delete(db:Session,resume_analysis:ResumeAnalysis):
        db.delete(resume_analysis)
        db.commit()