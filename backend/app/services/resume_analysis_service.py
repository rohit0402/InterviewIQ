from sqlalchemy.orm import Session

from app.ai.ai_service import AIService
from app.core.enum import ResumeStatus
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_analysis_repository import (
    ResumeAnalysisRepository,
)
from app.repositories.resume_repository import ResumeRepository
from app.services.pdf_service import PdfService


class ResumeAnalysisService:

    @staticmethod
    def analyze_resume(db: Session,resume: Resume,) -> ResumeAnalysis:
        resume.status = ResumeStatus.PROCESSING
        ResumeRepository.update(db, resume)
        text = ResumeAnalysisService.extract_resume_text(db,resume,)
        result = ResumeAnalysisService.run_ai_analysis(text,)
        analysis = ResumeAnalysisService.save_analysis(db,resume,result,)
        resume.status = ResumeStatus.COMPLETED
        ResumeRepository.update(db, resume)
        return analysis
    
    @staticmethod
    def extract_resume_text(db: Session,resume: Resume,) -> str:
        text = PdfService.extract_text(resume.file_path,)
        resume.raw_text = text
        ResumeRepository.update(db, resume)
        return text
    
    @staticmethod
    def run_ai_analysis(resume_text: str,):
        ai_service = AIService()
        return ai_service.analyze_resume(resume_text,)
    
    @staticmethod
    def save_analysis(db: Session,resume: Resume,result) -> ResumeAnalysis:
        analysis = ResumeAnalysisRepository.get_by_resume_id(db,resume.id,)
        is_new = analysis is None

        if is_new:
            analysis = ResumeAnalysis(resume_id=resume.id,)

        ResumeAnalysisService.populate_analysis(analysis,result,)

        if is_new:
            return ResumeAnalysisRepository.create(db,analysis,)

        return ResumeAnalysisRepository.update(db,analysis,)
    
    @staticmethod
    def populate_analysis(analysis: ResumeAnalysis,result,):
        analysis.summary = result.summary
        analysis.skills = result.skills
        analysis.education = [item.model_dump()for item in result.education]
        analysis.experience = [item.model_dump()for item in result.experience]
        analysis.projects = [item.model_dump()for item in result.projects]
        analysis.strengths = result.strengths
        analysis.weaknesses = result.weaknesses
        analysis.ats_score = result.ats_score