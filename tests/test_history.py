"""Tests for the history functionality."""

import pytest

from coverlettergenerator.app import app
from coverlettergenerator.models import CoverLetterHistory, db


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()


def test_get_empty_history(client):
    """Test getting history when no entries exist."""
    response = client.get("/history")
    assert response.status_code == 200
    data = response.get_json()
    assert data["history"] == []


def test_save_and_retrieve_history(client):
    """Test saving and retrieving a history entry."""
    # Create a test history entry
    with app.app_context():
        history_entry = CoverLetterHistory(
            company_name="Test Company",
            company_website="test.com",
            job_description="Test job description",
            cv_filename="test_cv.pdf",
            cv_content="Test CV content",
            generated_cover_letter="Test cover letter content",
        )
        db.session.add(history_entry)
        db.session.commit()

        # Retrieve history
        response = client.get("/history")
        assert response.status_code == 200
        data = response.get_json()
        assert len(data["history"]) == 1
        assert data["history"][0]["company_name"] == "Test Company"
        assert data["history"][0]["cv_filename"] == "test_cv.pdf"


def test_get_specific_history_entry(client):
    """Test retrieving a specific history entry."""
    with app.app_context():
        history_entry = CoverLetterHistory(
            company_name="Test Company",
            company_website="test.com",
            job_description="Test job description",
            cv_filename="test_cv.pdf",
            cv_content="Test CV content",
            generated_cover_letter="Test cover letter content",
        )
        db.session.add(history_entry)
        db.session.commit()

        # Retrieve specific entry
        response = client.get(f"/history/{history_entry.id}")
        assert response.status_code == 200
        data = response.get_json()
        assert data["company_name"] == "Test Company"
        assert data["generated_cover_letter"] == "Test cover letter content"


def test_clear_history(client):
    """Test clearing all history entries."""
    with app.app_context():
        # Create test entries
        entry1 = CoverLetterHistory(
            company_name="Company 1",
            job_description="Job 1",
            cv_filename="cv1.pdf",
            cv_content="CV 1 content",
            generated_cover_letter="Cover letter 1",
        )
        entry2 = CoverLetterHistory(
            company_name="Company 2",
            job_description="Job 2",
            cv_filename="cv2.pdf",
            cv_content="CV 2 content",
            generated_cover_letter="Cover letter 2",
        )
        db.session.add_all([entry1, entry2])
        db.session.commit()

        # Verify entries exist
        assert CoverLetterHistory.query.count() == 2

        # Clear history
        response = client.delete("/history/clear")
        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "History cleared successfully"

        # Verify entries are gone
        assert CoverLetterHistory.query.count() == 0


def test_get_nonexistent_history_entry(client):
    """Test retrieving a history entry that doesn't exist."""
    with app.app_context():
        response = client.get("/history/999")
        assert response.status_code == 404
