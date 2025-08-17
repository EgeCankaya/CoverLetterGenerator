# History Management

The Cover Letter Generator now includes a comprehensive history management system that allows users to save, view, and manage their previously generated cover letters.

## Features

### Automatic Saving
- Every generated cover letter is automatically saved to the local database
- CV content, job details, and generated cover letter are all preserved
- No manual intervention required

### History Viewing
- Click the "📋 View History" button in the header to access your history
- View all previously generated cover letters in chronological order
- See company name, CV filename, and generation date for each entry
- Preview the first 300 characters of each cover letter

### History Actions
- **View Full**: Click "👁️ View Full" to see the complete cover letter
- **Copy**: Click "📋 Copy" to copy the cover letter to clipboard
- **Clear All**: Use "🗑️ Clear All History" to remove all stored data

### Data Storage
- All data is stored locally in a SQLite database (`cover_letter_history.db`)
- No data is sent to external servers
- Database file is automatically created when you first generate a cover letter

## Database Schema

The history is stored in the `cover_letter_history` table with the following fields:

- `id`: Unique identifier for each entry
- `company_name`: Name of the company the cover letter was generated for
- `company_website`: Company website (if provided)
- `job_description`: The job description used for generation
- `cv_filename`: Original filename of the uploaded CV
- `cv_content`: Extracted text content from the CV
- `generated_cover_letter`: The complete generated cover letter
- `created_at`: Timestamp when the cover letter was generated

## API Endpoints

### GET /history
Retrieves all history entries ordered by creation date (newest first).

**Response:**
```json
{
  "history": [
    {
      "id": 1,
      "company_name": "Example Corp",
      "company_website": "example.com",
      "job_description": "Software Engineer position...",
      "cv_filename": "my_cv.pdf",
      "generated_cover_letter": "Dear Hiring Manager...",
      "created_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### GET /history/{id}
Retrieves a specific history entry by ID.

**Response:**
```json
{
  "id": 1,
  "company_name": "Example Corp",
  "company_website": "example.com",
  "job_description": "Software Engineer position...",
  "cv_filename": "my_cv.pdf",
  "generated_cover_letter": "Dear Hiring Manager...",
  "created_at": "2024-01-15T10:30:00"
}
```

### DELETE /history/clear
Clears all history entries.

**Response:**
```json
{
  "message": "History cleared successfully"
}
```

## Privacy and Security

- All data is stored locally on your machine
- No data is transmitted to external servers
- The database file can be deleted at any time to remove all history
- Use the "Clear All History" feature to remove all stored data

## Technical Implementation

### Dependencies Added
- `flask-sqlalchemy`: Database ORM for Flask
- `flask-migrate`: Database migration support (for future use)

### Files Modified
- `app.py`: Added database configuration and new API endpoints
- `models.py`: New file defining the database model
- `templates/index.html`: Added history UI components
- `static/css/style.css`: Added styling for history components
- `static/js/app.js`: Added history management JavaScript
- `__init__.py`: Updated to export new models
- `pyproject.toml`: Added new dependencies
- `.gitignore`: Added database file exclusion

### Database Setup
The database is automatically created when the application starts for the first time. The SQLite database file (`cover_letter_history.db`) will be created in the application's root directory.
