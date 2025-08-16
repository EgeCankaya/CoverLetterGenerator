"""AI-powered cover letter generation using Google Gemini API."""

import os

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MissingAPIKeyError(ValueError):
    """Raised when the Gemini API key is not set."""

    def __init__(self):
        super().__init__("GEMINI_API_KEY environment variable is required")


class CoverLetterGenerator:
    """Generates personalized cover letters using AI."""

    def __init__(self):
        """Initialize the cover letter generator with Gemini client."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise MissingAPIKeyError()

        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(self, cv_content: str, company_name: str, company_website: str = "", job_description: str = "") -> str:
        """
        Generate a personalized cover letter based on CV and job details.

        Args:
            cv_content: Extracted text from the user's CV
            company_name: Name of the target company
            company_website: Company website (optional)
            job_description: Job description and requirements

        Returns:
            Generated cover letter text
        """
        try:
            # Create the prompt for the AI
            prompt = self._create_prompt(
                cv_content=cv_content,
                company_name=company_name,
                company_website=company_website,
                job_description=job_description,
            )

            # Generate the cover letter using Gemini
            response = self.model.generate_content(prompt)

            if response.text:
                return response.text.strip()
            else:
                return self._get_fallback_cover_letter(company_name)

        except Exception as e:
            print(f"Error generating cover letter: {e!s}")
            return self._get_fallback_cover_letter(company_name)

    def _create_prompt(self, cv_content: str, company_name: str, company_website: str, job_description: str) -> str:
        """Create a detailed prompt for the AI model."""

        prompt = f"""
Please write a professional cover letter for the following job application:

COMPANY: {company_name}
{f"WEBSITE: {company_website}" if company_website else ""}

JOB DESCRIPTION:
{job_description}

CANDIDATE'S CV/RESUME:
{cv_content}

INSTRUCTIONS:
1. Create a compelling, professional cover letter that connects the candidate's experience with the job requirements
2. Use a formal, business-appropriate tone
3. Include specific examples from their CV that relate to the job description
4. Keep it concise but impactful (around 300-400 words)
5. Start with a strong opening that mentions the specific position and company
6. Include a clear call-to-action in the closing paragraph
7. Format it as a proper business letter with appropriate spacing

Please generate the cover letter now:
"""
        return prompt.strip()

    def _get_fallback_cover_letter(self, company_name: str) -> str:
        """Return a fallback cover letter if AI generation fails."""
        return f"""
Dear Hiring Manager,

I am writing to express my interest in the position at {company_name}. I am excited about the opportunity to contribute to your team and believe my skills and experience would be a valuable addition to your organization.

Throughout my career, I have demonstrated strong problem-solving abilities and a commitment to delivering high-quality results. I am particularly drawn to {company_name} because of its reputation for innovation and excellence in the industry.

I would welcome the opportunity to discuss how my background, skills, and enthusiasm would make me a valuable member of your team. Thank you for considering my application.

Sincerely,
[Your Name]
"""
