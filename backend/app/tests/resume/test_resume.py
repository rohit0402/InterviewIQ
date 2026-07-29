from app.services.resume_service import ResumeService
from app.tests.utils.auth import authenticated_user
import io



def test_get_resume_success(client, monkeypatch, tmp_path):
    user, token = authenticated_user(client)

    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"%PDF-1.4 Dummy PDF")

    def fake_save_resume(file):
        return ("resume.pdf", str(resume_path))

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.save_resume",
        fake_save_resume,
    )

    monkeypatch.setattr(
        "app.services.resume_service.process_resume_task.delay",
        lambda resume_id: None,
    )

    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "file": (
                "resume.pdf",
                io.BytesIO(b"%PDF"),
                "application/pdf",
            )
        },
    )

    response = client.get(
        "/api/v1/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["original_filename"] == "resume.pdf"

def test_get_resume_not_found(client):
    user, token = authenticated_user(client)

    response = client.get(
        "/api/v1/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"

def test_get_resume_without_login(client):
    response = client.get("/api/v1/resumes")

    assert response.status_code == 401

def test_get_analysis_without_resume(client):
    user, token = authenticated_user(client)

    response = client.get(
        "/api/v1/resumes/analysis",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404

def test_get_analysis_without_login(client):
    response = client.get("/api/v1/resumes/analysis")

    assert response.status_code == 401


def test_delete_resume(client, monkeypatch, tmp_path):
    user, token = authenticated_user(client)

    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"%PDF-1.4 Dummy PDF")

    def fake_save_resume(file):
        return ("resume.pdf", str(resume_path))

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.save_resume",
        fake_save_resume,
    )
    monkeypatch.setattr(
        "app.services.resume_service.process_resume_task.delay",
        lambda resume_id: None,
    )

    deleted = []

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.delete_resume",
        lambda path: deleted.append(path),
    )

    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={
            "file": (
                "resume.pdf",
                io.BytesIO(b"%PDF"),
                "application/pdf",
            )
        },
    )

    response = client.delete(
        "/api/v1/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204
    assert len(deleted) == 1

def test_delete_resume_not_found(client):
    user, token = authenticated_user(client)

    response = client.delete(
        "/api/v1/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404

def test_delete_resume_without_login(client):
    response = client.delete("/api/v1/resumes")

    assert response.status_code == 401