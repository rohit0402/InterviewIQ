from app.core.config import settings

def test_client_fixture(client):
    response = client.get(f"{settings.api_v1_prefix}/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "project_name": settings.project_name,
        "version": settings.version,
    }