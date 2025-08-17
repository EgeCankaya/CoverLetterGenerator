"""Main Flask application for the AI Cover Letter Generator."""

import tempfile

from flask import Flask, jsonify, render_template, request, send_from_directory

from .cover_letter_generator import CoverLetterGenerator
from .file_processor import FileProcessor
from .models import CoverLetterHistory, db

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["UPLOAD_FOLDER"] = tempfile.mkdtemp()

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cover_letter_history.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Initialize components
file_processor = FileProcessor()
cover_letter_generator = CoverLetterGenerator()

# Create database tables
with app.app_context():
    db.create_all()


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

        # Save to history
        history_entry = CoverLetterHistory(
            company_name=company_name,
            company_website=company_website,
            job_description=job_description,
            cv_filename=cv_file.filename,
            cv_content=cv_content,
            generated_cover_letter=cover_letter,
        )
        db.session.add(history_entry)
        db.session.commit()

        return jsonify({"cover_letter": cover_letter, "history_id": history_entry.id})

    except Exception:
        app.logger.exception("Error generating cover letter")
        return jsonify({"error": "An error occurred while generating the cover letter"}), 500


@app.route("/history")
def get_history():
    """Get all cover letter history entries."""
    try:
        history_entries = CoverLetterHistory.query.order_by(CoverLetterHistory.created_at.desc()).all()

        return jsonify({"history": [entry.to_dict() for entry in history_entries]})
    except Exception:
        app.logger.exception("Error retrieving history")
        return jsonify({"error": "An error occurred while retrieving history"}), 500


@app.route("/history/<int:history_id>")
def get_history_entry(history_id):
    """Get a specific history entry."""
    try:
        entry = CoverLetterHistory.query.get_or_404(history_id)
        return jsonify(entry.to_dict())
    except Exception as e:
        # Don't catch 404 errors, let them propagate
        if hasattr(e, "code") and e.code == 404:
            raise
        app.logger.exception(f"Error retrieving history entry {history_id}")
        return jsonify({"error": "An error occurred while retrieving the history entry"}), 500


@app.route("/history/clear", methods=["DELETE"])
def clear_history():
    """Clear all history entries."""
    try:
        CoverLetterHistory.query.delete()
        db.session.commit()
        return jsonify({"message": "History cleared successfully"})
    except Exception:
        app.logger.exception("Error clearing history")
        db.session.rollback()
        return jsonify({"error": "An error occurred while clearing history"}), 500


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files."""
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
