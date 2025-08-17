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
        self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

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
                # Post-process to remove brackets from personal information
                processed_text = self._remove_brackets_from_personal_info(response.text.strip())
                return processed_text
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

CRITICAL INSTRUCTIONS:
1. Extract the candidate's personal information from their CV:
   - Full name (use this directly in the signature without any brackets)
   - Address (include in the header if present)
   - Phone number (include in the header if present)
   - Email address (include in the header if present)

2. Create a compelling, professional cover letter that connects the candidate's experience with the job requirements
3. Use a formal, business-appropriate tone
4. Include specific examples from their CV that relate to the job description
5. Keep it concise but impactful (around 300-400 words)
6. Start with a strong opening that mentions the specific position and company
7. Include a clear call-to-action in the closing paragraph
8. Format it as a proper business letter with appropriate spacing

CRITICAL: NEVER use brackets [ ] or parentheses ( ) around names, addresses, phone numbers, or email addresses. Write all personal information directly without any formatting.

IMPORTANT: When using the candidate's name in the signature, write it directly without any brackets, parentheses, or other formatting. For example, if the CV shows "John Doe", write "Sincerely, John Doe" - NOT "Sincerely, [John Doe]" or "Sincerely, (John Doe)".

FORMAT EXAMPLE:
If the CV contains: "JANE SMITH" and "123 Main St, City, State"
The signature should be: "Sincerely, Jane Smith" (no brackets, no parentheses)

REMEMBER: NO BRACKETS ANYWHERE in the cover letter. Write all information directly.

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
[Please add your name here]
"""

    def _remove_brackets_from_personal_info(self, text: str) -> str:
        """Remove brackets from personal information in the generated text."""
        import re

        # Remove brackets from names in signatures
        # Pattern: "Sincerely," followed by bracketed text
        text = re.sub(r"(Sincerely,?\s*)\[([^\]]+)\]", r"\1\2", text)

        # Remove brackets from names in headers
        # Pattern: bracketed text that looks like a name (capitalized words)
        text = re.sub(r"\[([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\]", r"\1", text)

        # Remove brackets from addresses
        # Pattern: bracketed text that contains common address elements
        address_patterns = [
            r"\[([0-9]+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[^]]*)\]",
            r"\[([A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd)[^]]*)\]",
        ]

        for pattern in address_patterns:
            text = re.sub(pattern, r"\1", text)

        # Remove brackets from phone numbers
        text = re.sub(r"\[((?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4})\]", r"\1", text)

        # Remove brackets from email addresses
        text = re.sub(r"\[([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\]", r"\1", text)

        return text
