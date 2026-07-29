import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.database.base import Base
from app.database.dependencies import get_db
from app.main import create_app

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)

assert "interviewiq_test" in settings.database_url

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(autouse=True)
def clean_database():
    db = TestingSessionLocal()

    try:
        # Clean before test
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

        yield

        # Clean after test
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()

    finally:
        db.close()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client