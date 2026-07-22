from app.ai import ai_service

resume = """
Rohit Sonar

Python
FastAPI
PostgreSQL
React
1200+ DSA problems

Built InterviewIQ backend.
"""

analysis = ai_service.analyze_resume(resume)
