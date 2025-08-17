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

    @patch("coverlettergenerator.cover_letter_generator.os.getenv")
    @patch("coverlettergenerator.cover_letter_generator.genai")
    def test_generate_cover_letter_with_personal_info(self, mock_genai, mock_getenv):
        """Test that personal information is extracted from CV."""
        mock_getenv.return_value = "test_api_key"

        # Mock the Gemini model and response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = """John Doe
123 Main Street, City, State 12345
Phone: (555) 123-4567
Email: john.doe@email.com

Dear Hiring Manager,

I am writing to express my interest in the position at Test Company...

Sincerely,
John Doe"""
        mock_model.generate_content.return_value = mock_response
        mock_genai.GenerativeModel.return_value = mock_model

        generator = CoverLetterGenerator()

        cv_content = """
        JOHN DOE
        123 Main Street, City, State 12345
        Phone: (555) 123-4567
        Email: john.doe@email.com

        EXPERIENCE:
        Software Engineer at Tech Corp (2020-2023)
        """

        generator.generate(
            cv_content=cv_content,
            company_name="Test Company",
            company_website="https://test.com",
            job_description="Software Engineer position",
        )

        # Verify that the AI was instructed to extract personal information
        mock_model.generate_content.assert_called_once()
        call_args = mock_model.generate_content.call_args[0][0]
        assert "Extract the candidate's personal information" in call_args
        assert "Full name" in call_args
        assert "Address" in call_args
        assert "Phone number" in call_args
        assert "Email address" in call_args
        assert "without any brackets" in call_args
        assert "FORMAT EXAMPLE" in call_args
        assert "NEVER use brackets" in call_args
        assert "NO BRACKETS ANYWHERE" in call_args

    def test_remove_brackets_from_personal_info(self):
        """Test that brackets are removed from personal information."""
        from coverlettergenerator.cover_letter_generator import CoverLetterGenerator

        # Create a mock generator to test the bracket removal method
        with patch("coverlettergenerator.cover_letter_generator.os.getenv") as mock_getenv:
            mock_getenv.return_value = "test_api_key"
            generator = CoverLetterGenerator()

        # Test cases for bracket removal
        test_cases = [
            # Names in signatures
            ("Sincerely,\n[John Doe]", "Sincerely,\nJohn Doe"),
            ("Sincerely, [Jane Smith]", "Sincerely, Jane Smith"),
            # Names in headers
            ("[John Doe]\n123 Main St", "John Doe\n123 Main St"),
            ("[Jane Smith]\n456 Oak Ave", "Jane Smith\n456 Oak Ave"),
            # Addresses
            ("[123 Main Street, City, State 12345]", "123 Main Street, City, State 12345"),
            ("[456 Oak Avenue, Town, ST 67890]", "456 Oak Avenue, Town, ST 67890"),
            # Phone numbers
            ("[(555) 123-4567]", "(555) 123-4567"),
            ("[+1-555-123-4567]", "+1-555-123-4567"),
            # Email addresses
            ("[john.doe@email.com]", "john.doe@email.com"),
            ("[jane.smith@company.org]", "jane.smith@company.org"),
            # Mixed content
            (
                "[John Doe]\n[123 Main St]\n[(555) 123-4567]\n[john@email.com]",
                "John Doe\n123 Main St\n(555) 123-4567\njohn@email.com",
            ),
        ]

        for input_text, expected_output in test_cases:
            result = generator._remove_brackets_from_personal_info(input_text)
            assert result == expected_output, f"Failed for input: {input_text}"


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
        mock_doc.tables = []  # No tables in this test
        mock_document.return_value = mock_doc

        # Mock file object
        mock_file = Mock()
        mock_file.filename = "test.docx"

        result = processor.extract_text(mock_file)

        assert result == "First paragraph\nSecond paragraph"

    @patch("coverlettergenerator.file_processor.Document")
    def test_extract_from_docx_with_tables(self, mock_document):
        """Test DOCX text extraction including tables."""
        processor = FileProcessor()

        # Mock the document with paragraphs and tables
        mock_doc = Mock()
        mock_paragraph1 = Mock()
        mock_paragraph1.text = "Name: John Doe"
        mock_paragraph2 = Mock()
        mock_paragraph2.text = "Experience:"

        mock_doc.paragraphs = [mock_paragraph1, mock_paragraph2]

        # Mock table
        mock_table = Mock()
        mock_row1 = Mock()
        mock_cell1 = Mock()
        mock_cell1.text = "Company"
        mock_cell2 = Mock()
        mock_cell2.text = "Position"
        mock_cell3 = Mock()
        mock_cell3.text = "Duration"

        mock_row1.cells = [mock_cell1, mock_cell2, mock_cell3]
        mock_table.rows = [mock_row1]
        mock_doc.tables = [mock_table]

        mock_document.return_value = mock_doc

        # Mock file object
        mock_file = Mock()
        mock_file.filename = "test.docx"

        result = processor.extract_text(mock_file)

        expected = "Name: John Doe\nExperience:\nCompany | Position | Duration"
        assert result == expected

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
