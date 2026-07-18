from sqlalchemy.orm import Session
from app.models.resume_analysis import ResumeAnalysis
from app.repositories.resume_analysis_repository import ResumeAnalysisRepository

from app.services.pdf_service import PdfService

class ResumeAnalysisService:
    @staticmethod
    def analyze_resume(db:Session,resume):
        text=PdfService.extract_text(resume.file_path)
        existing_analysis=ResumeAnalysisRepository.get_by_resume_id(db,resume.id)

        if existing_analysis:
            existing_analysis.raw_text=text

            return ResumeAnalysisRepository.update(db,existing_analysis)
        
        analysis=ResumeAnalysis(
            resume_id=resume.id,
            raw_text=text
        )
        return ResumeAnalysisRepository.create(db,analysis)
