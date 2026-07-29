import io

from app.tests.utils.auth import authenticated_user


def test_upload_resume_success(client, monkeypatch, tmp_path):
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

    data = {
        "file": (
            "resume.pdf",
            io.BytesIO(b"%PDF-1.4 test pdf"),
            "application/pdf",
        )
    }

    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=data,
    )

    assert response.status_code == 202

    body = response.json()

    assert body["original_filename"] == "resume.pdf"
    assert body["mime_type"] == "application/pdf"
    assert body["analysis_available"] is False


def test_upload_resume_unauthorized(client):
    data = {
        "file": (
            "resume.pdf",
            io.BytesIO(b"%PDF"),
            "application/pdf",
        )
    }

    response = client.post(
        "/api/v1/resumes/upload",
        files=data,
    )

    assert response.status_code == 401


def test_upload_invalid_file(client):
    user, token = authenticated_user(client)

    data = {
        "file": (
            "notes.txt",
            io.BytesIO(b"hello"),
            "text/plain",
        )
    }

    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=data,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed"


def test_upload_without_file(client):
    user, token = authenticated_user(client)

    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 422


def test_replace_existing_resume(client, monkeypatch, tmp_path):
    user, token = authenticated_user(client)

    deleted = []

    new_path = tmp_path / "new.pdf"
    new_path.write_bytes(b"dummy")

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.save_resume",
        lambda file: ("new.pdf", str(new_path)),
    )

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.delete_resume",
        lambda path: deleted.append(path),
    )

    monkeypatch.setattr(
        "app.services.resume_service.process_resume_task.delay",
        lambda resume_id: None,
    )

    file = {
        "file": (
            "resume.pdf",
            io.BytesIO(b"%PDF"),
            "application/pdf",
        )
    }

    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=file,
    )

    client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=file,
    )

    assert len(deleted) == 1


def test_upload_celery_failure(client, monkeypatch, tmp_path):
    user, token = authenticated_user(client)

    resume_path = tmp_path / "resume.pdf"
    resume_path.write_bytes(b"%PDF-1.4 Dummy PDF")

    def fake_save_resume(file):
        return ("resume.pdf", str(resume_path))

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.save_resume",
        fake_save_resume,
    )

    def fail(_):
        raise Exception("Celery down")

    monkeypatch.setattr(
        "app.services.resume_service.process_resume_task.delay",
        fail,
    )

    deleted = []

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.delete_resume",
        lambda path: deleted.append(path),
    )

    data = {
        "file": (
            "resume.pdf",
            io.BytesIO(b"%PDF"),
            "application/pdf",
        )
    }

    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=data,
    )

    assert response.status_code == 500
    assert len(deleted) == 1


def test_upload_storage_failure(client, monkeypatch):
    user, token = authenticated_user(client)

    def fail(_):
        raise Exception("Disk full")

    monkeypatch.setattr(
        "app.services.resume_service.FileStorage.save_resume",
        fail,
    )

    data = {
        "file": (
            "resume.pdf",
            io.BytesIO(b"%PDF"),
            "application/pdf",
        )
    }

    response = client.post(
        "/api/v1/resumes/upload",
        headers={"Authorization": f"Bearer {token}"},
        files=data,
    )

    assert response.status_code == 500