"""Main entry point for the AI Cover Letter Generator application."""

import os
import sys

from coverlettergenerator.app import app


def main() -> None:
    """Run the Flask application."""
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set your Gemini API key:")
        print("1. Get your API key from https://makersuite.google.com/app/apikey")
        print("2. Create a .env file in the project root with:")
        print("   GEMINI_API_KEY=your_gemini_api_key_here")
        print("3. Or set the environment variable directly:")
        print("   export GEMINI_API_KEY=your_gemini_api_key_here")
        sys.exit(1)

    print("🚀 Starting AI Cover Letter Generator...")
    print("📝 Upload your CV, add job details, and get a personalized cover letter!")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print()

    try:
        app.run(debug=False, host="127.0.0.1", port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
