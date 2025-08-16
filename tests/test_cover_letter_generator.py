"""Tests for the AI Cover Letter Generator."""

from unittest.mock import Mock, patch

import pytest

from coverlettergenerator.cover_letter_generator import CoverLetterGenerator
from coverlettergenerator.file_processor import FileProcessor


class TestCoverLetterGenerator:
    """Test cases for the CoverLetterGenerator class."""

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    @patch("coverlettergenerator.cover_letter_generator.genai")
    def test_init_with_api_key(self, mock_genai, mock_getenv):
        """Test initialization with valid API key."""
        mock_getenv.return_value = "test_api_key"

        generator = CoverLetterGenerator()
        assert generator.model is not None
        mock_genai.configure.assert_called_once_with(api_key="test_api_key")

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    def test_init_without_api_key(self, mock_getenv):
        """Test initialization without API key raises error."""
        mock_getenv.return_value = None

        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable is required"):
            CoverLetterGenerator()

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    @patch("coverlettergenerator.cover_letter_generator.genai")
    def test_generate_cover_letter_success(self, mock_genai, mock_getenv):
        """Test successful cover letter generation."""
        mock_getenv.return_value = "test_api_key"

        # Mock the Gemini model and response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "Dear Hiring Manager,\n\nTest cover letter content."
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        generator = CoverLetterGenerator()

        result = generator.generate(
            cv_content="Test CV content",
            company_name="Test Company",
            company_website="https://test.com",
            job_description="Test job description",
        )

        assert "Dear Hiring Manager" in result
        assert "Test cover letter content" in result

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    @patch("coverlettergenerator.cover_letter_generator.genai")
    def test_generate_cover_letter_fallback(self, mock_genai, mock_getenv):
        """Test fallback cover letter when AI generation fails."""
        mock_getenv.return_value = "test_api_key"

        # Mock the Gemini model to raise an exception
        mock_model = Mock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_genai.GenerativeModel.return_value = mock_model

        generator = CoverLetterGenerator()

        result = generator.generate(
            cv_content="Test CV content", company_name="Test Company", job_description="Test job description"
        )

        assert "Test Company" in result
        assert "Dear Hiring Manager" in result

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    @patch("coverlettergenerator.cover_letter_generator.genai")
    def test_generate_cover_letter_empty_response(self, mock_genai, mock_getenv):
        """Test fallback when Gemini returns empty response."""
        mock_getenv.return_value = "test_api_key"

        # Mock the Gemini model to return empty response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = ""
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        generator = CoverLetterGenerator()

        result = generator.generate(
            cv_content="Test CV content", company_name="Test Company", job_description="Test job description"
        )

        assert "Test Company" in result
        assert "Dear Hiring Manager" in result


class TestFileProcessor:
    """Test cases for the FileProcessor class."""

    def test_is_valid_file_pdf(self):
        """Test PDF file validation."""
        processor = FileProcessor()
        assert processor.is_valid_file("test.pdf") is True
        assert processor.is_valid_file("test.PDF") is True

    def test_is_valid_file_docx(self):
        """Test DOCX file validation."""
        processor = FileProcessor()
        assert processor.is_valid_file("test.docx") is True
        assert processor.is_valid_file("test.DOCX") is True

    def test_is_valid_file_invalid(self):
        """Test invalid file validation."""
        processor = FileProcessor()
        assert processor.is_valid_file("test.txt") is False
        assert processor.is_valid_file("test.jpg") is False
        assert processor.is_valid_file("") is False
        assert processor.is_valid_file(None) is False

    @patch("coverlettergenerator.file_processor.Document")
    def test_extract_from_docx(self, mock_document):
        """Test DOCX text extraction."""
        processor = FileProcessor()

        # Mock the document and paragraphs
        mock_doc = Mock()
        mock_paragraph1 = Mock()
        mock_paragraph1.text = "First paragraph"
        mock_paragraph2 = Mock()
        mock_paragraph2.text = "Second paragraph"
        mock_paragraph3 = Mock()
        mock_paragraph3.text = ""  # Empty paragraph should be ignored

        mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2, mock_paragraph3]
        mock_document.return_value = mock_doc

        # Mock file object
        mock_file = Mock()
        mock_file.filename = "test.docx"

        result = processor.extract_text(mock_file)

        assert result == "First paragraph\nSecond paragraph"

    @patch("coverlettergenerator.file_processor.PdfReader")
    def test_extract_from_pdf(self, mock_pdf_reader):
        """Test PDF text extraction."""
        processor = FileProcessor()

        # Mock the PDF reader and pages
        mock_reader = Mock()
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "First page"
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Second page"

        mock_reader.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader

        # Mock file object
        mock_file = Mock()
        mock_file.filename = "test.pdf"

        result = processor.extract_text(mock_file)

        assert result == "First page\nSecond page"
