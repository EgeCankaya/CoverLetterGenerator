"""Main Flask application for the AI Cover Letter Generator."""

import tempfile

from flask import Flask, jsonify, render_template, request, send_from_directory

from .cover_letter_generator import CoverLetterGenerator
from .file_processor import FileProcessor

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()

# Initialize components
file_processor = FileProcessor()
cover_letter_generator = CoverLetterGenerator()


@app.route("/")
def index():
    """Render the main application page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_cover_letter():
    """Generate a cover letter based on uploaded CV and job details."""
    try:
        # Check if CV file was uploaded
        if "cv_file" not in request.files:
            return jsonify({"error": "No CV file uploaded"}), 400

        cv_file = request.files["cv_file"]
        if cv_file.filename == "":
            return jsonify({"error": "No CV file selected"}), 400

        # Validate file type
        if not file_processor.is_valid_file(cv_file.filename):
            return jsonify({"error": "Invalid file type. Please upload PDF or DOCX files only."}), 400

        # Get form data
        company_name = request.form.get("company_name", "").strip()
        company_website = request.form.get("company_website", "").strip()
        job_description = request.form.get("job_description", "").strip()

        # Validate required fields
        if not company_name:
            return jsonify({"error": "Company name is required"}), 400
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400

        # Process CV file
        cv_content = file_processor.extract_text(cv_file)
        if not cv_content:
            return jsonify({"error": "Could not extract text from CV file"}), 400

        # Generate cover letter
        cover_letter = cover_letter_generator.generate(
            cv_content=cv_content,
            company_name=company_name,
            company_website=company_website,
            job_description=job_description,
        )

        return jsonify({"cover_letter": cover_letter})

    except Exception:
        app.logger.exception("Error generating cover letter")
        return jsonify({"error": "An error occurred while generating the cover letter"}), 500


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files."""
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
