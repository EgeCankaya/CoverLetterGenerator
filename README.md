# AI Cover Letter Generator

A local Python application that uses AI to instantly generate personalized cover letters from your CV and a specific job description.

## 🚀 Features

- **AI-Powered Generation**: Uses Google's Gemini 1.5 Flash to create compelling, personalized cover letters
- **CV Upload Support**: Accepts PDF and DOCX files
- **Local Processing**: All data stays on your machine - no information is stored on external servers
- **Modern Web Interface**: Clean, responsive design with drag-and-drop file upload
- **Instant Results**: Generate professional cover letters in seconds
- **Copy to Clipboard**: Easy one-click copying of generated letters

## 📋 Requirements

- Python 3.9 or higher
- Google Gemini API key
- Modern web browser

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EgeCankaya/CoverLetterGenerator.git
   cd CoverLetterGenerator
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -e .
   ```

3. **Set up your Google Gemini API key**:

   Create a `.env` file in the project root:
   ```bash
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

   Or set the environment variable directly:
   ```bash
   export GEMINI_API_KEY=your_gemini_api_key_here
   ```

   **Get your API key from**: https://makersuite.google.com/app/apikey

## 🚀 Usage

### Running the Application

1. **Start the server**:
   ```bash
   # Using Python module
   python -m coverlettergenerator

   # Or directly
   python coverlettergenerator/__main__.py
   ```

2. **Open your browser** and go to: http://localhost:5000

3. **Upload your CV** (PDF or DOCX format)

4. **Fill in the job details**:
   - Company name (required)
   - Company website (optional)
   - Job description (required)

5. **Click "Generate Cover Letter"** and wait for the AI to create your personalized letter

6. **Copy the generated letter** to your clipboard and paste it into your preferred document editor

### Example Workflow

1. **Prepare your CV**: Make sure your CV is in PDF or DOCX format
2. **Find a job posting**: Copy the job description from the posting
3. **Generate the letter**: Use the web interface to upload your CV and paste the job description
4. **Review and edit**: The AI generates a first draft - review and make any necessary edits
5. **Submit**: Use the final version for your job application

## 🏗️ Architecture

The application is built with a simple, modular architecture:

- **Frontend**: HTML, CSS, JavaScript with a modern, responsive design
- **Backend**: Flask web server handling file uploads and API requests
- **AI Integration**: Google Gemini 1.5 Flash for cover letter generation
- **File Processing**: Support for PDF and DOCX CV files
- **Security**: All processing happens locally with no data storage

### Project Structure

```
CoverLetterGenerator/
├── coverlettergenerator/
│   ├── __init__.py
│   ├── __main__.py              # Application entry point
│   ├── app.py                   # Flask application
│   ├── cover_letter_generator.py # AI integration
│   ├── file_processor.py        # File handling utilities
│   ├── templates/
│   │   └── index.html          # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css       # Styling
│       └── js/
│           └── app.js          # Frontend functionality
├── tests/                      # Test suite
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
└── README.md                  # This file
```

## 🔧 Development

### Setting up the development environment

1. **Install development dependencies**:
   ```bash
   uv sync --group dev
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Run linting**:
   ```bash
   ruff check .
   ruff format .
   ```

4. **Run type checking**:
   ```bash
   mypy coverlettergenerator
   ```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 🔒 Privacy & Security

- **Local Processing**: All CV files and generated content are processed locally
- **No Data Storage**: No files or personal information are stored on any servers
- **Secure API Calls**: Only the necessary text content is sent to Google Gemini for processing
- **Temporary Files**: Uploaded files are processed in memory and immediately discarded

## 🎯 MVP Features

This MVP focuses on the core functionality:

✅ **Core Features**:
- CV upload (PDF/DOCX)
- Job details input (company name, website, description)
- AI-powered cover letter generation
- Copy to clipboard functionality
- Modern, responsive web interface

❌ **Out of Scope** (for MVP):
- User accounts and login
- Saving or storing CVs or generated letters
- Rich text editor for modifying output
- Export to PDF or other formats
- ATS checker or score
- Payment or subscription features
- Multiple templates or style options

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/EgeCankaya/CoverLetterGenerator/issues)
3. Create a new issue with detailed information about your problem

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- AI powered by [Google Gemini](https://ai.google.dev/)
- Modern UI with [Inter font](https://rsms.me/inter/)
- File processing with [python-docx](https://python-docx.readthedocs.io/) and [PyPDF2](https://pypdf2.readthedocs.io/)

---

**Made with ❤️ by Egemen Çankaya**
