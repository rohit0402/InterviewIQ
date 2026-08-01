from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print("DATABASE_URL =", settings.database_url)
engine = create_engine(settings.database_url,echo=settings.debug,)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)