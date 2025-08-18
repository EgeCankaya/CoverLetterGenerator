"""Database models for the Cover Letter Generator."""

from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class CoverLetterHistory(db.Model):  # type: ignore[name-defined]
    """Model for storing cover letter generation history."""

    __tablename__ = "cover_letter_history"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    company_website = db.Column(db.String(500))
    job_description = db.Column(db.Text, nullable=False)
    cv_filename = db.Column(db.String(255), nullable=False)
    cv_content = db.Column(db.Text, nullable=False)
    generated_cover_letter = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict[str, str | int | None]:
        """Convert model to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "company_name": self.company_name,
            "company_website": self.company_website,
            "job_description": self.job_description,
            "cv_filename": self.cv_filename,
            "generated_cover_letter": self.generated_cover_letter,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
