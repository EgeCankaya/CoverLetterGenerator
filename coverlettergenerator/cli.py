"""Command-line interface for the AI Cover Letter Generator."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from .cover_letter_generator import CoverLetterGenerator
from .file_processor import FileProcessor


def validate_api_key() -> None:
    """Validate that the Gemini API key is set."""
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is required.")
        print("Please set your Gemini API key:")
        print("1. Get your API key from https://makersuite.google.com/app/apikey")
        print("2. Create a .env file with: GEMINI_API_KEY=your_gemini_api_key_here")
        print("3. Or set the environment variable: export GEMINI_API_KEY=your_gemini_api_key_here")
        sys.exit(1)


def validate_cv_file(cv_path: Path) -> None:
    """Validate that the CV file exists and is valid."""
    if not cv_path.exists():
        print(f"❌ Error: CV file not found: {cv_path}")
        sys.exit(1)


def process_cv_file(cv_path: Path, file_processor: FileProcessor) -> str:
    """Process the CV file and extract text."""
    print("📄 Processing CV file...")
    try:
        with open(cv_path, "rb") as f:
            cv_content = file_processor.extract_text(f)

        if not cv_content:
            print("❌ Error: Could not extract text from CV file.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing CV file: {e}")
        sys.exit(1)

    return cv_content


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI Cover Letter Generator - Generate personalized cover letters using AI"
    )

    parser.add_argument("--cv-file", "-c", required=True, help="Path to your CV file (PDF or DOCX)")

    parser.add_argument("--company", "-co", required=True, help="Company name")

    parser.add_argument("--website", "-w", help="Company website (optional)")

    parser.add_argument("--job-description", "-j", required=True, help="Job description text")

    parser.add_argument("--output", "-o", help="Output file path (optional, prints to console if not specified)")

    parser.add_argument("--env-file", "-e", help="Path to .env file (default: .env in current directory)")

    args = parser.parse_args()

    # Load environment variables
    env_file = args.env_file or ".env"
    if os.path.exists(env_file):
        load_dotenv(env_file)
    else:
        print(f"Warning: {env_file} not found. Make sure GEMINI_API_KEY is set in environment.")

    # Validate API key
    validate_api_key()

    # Validate CV file
    cv_path = Path(args.cv_file)
    validate_cv_file(cv_path)

    # Initialize components
    try:
        file_processor = FileProcessor()
        cover_letter_generator = CoverLetterGenerator()
    except Exception as e:
        print(f"❌ Error initializing components: {e}")
        sys.exit(1)

    # Validate file type
    if not file_processor.is_valid_file(cv_path.name):
        print("❌ Error: Invalid file type. Please use PDF or DOCX files.")
        sys.exit(1)

    # Process CV file
    cv_content = process_cv_file(cv_path, file_processor)

    # Generate cover letter
    print("🤖 Generating cover letter...")
    try:
        cover_letter = cover_letter_generator.generate(
            cv_content=cv_content,
            company_name=args.company,
            company_website=args.website or "",
            job_description=args.job_description,
        )
    except Exception as e:
        print(f"❌ Error generating cover letter: {e}")
        sys.exit(1)

    # Output result
    if args.output:
        output_path = Path(args.output)
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cover_letter)
            print(f"✅ Cover letter saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            sys.exit(1)
    else:
        print("\n" + "=" * 50)
        print("GENERATED COVER LETTER")
        print("=" * 50)
        print(cover_letter)
        print("=" * 50)


if __name__ == "__main__":
    main()
