"""AI Cover Letter Generator - A local Python application for generating personalized cover letters."""

__version__ = "0.0.1"
__author__ = "Egemen Cankaya"
__email__ = "egemencankaya14@gmail.com"

from .models import CoverLetterHistory, db

__all__ = ["CoverLetterHistory", "db"]
