import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.base import Base
from app.database.dependencies import get_db
from app.main import create_app

from app.core.config import settings
from sqlalchemy import create_engine

engine = create_engine(settings.database_url)
TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)

    if os.path.exists("test.db"):
        os.remove("test.db")


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