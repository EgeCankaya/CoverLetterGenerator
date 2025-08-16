// AI Cover Letter Generator - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('coverLetterForm');
    const cvFileInput = document.getElementById('cvFile');
    const fileInfo = document.getElementById('fileInfo');
    const generateBtn = document.getElementById('generateBtn');
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('errorSection');
    const coverLetterText = document.getElementById('coverLetterText');
    const copyBtn = document.getElementById('copyBtn');
    const newLetterBtn = document.getElementById('newLetterBtn');

    // File upload handling
    cvFileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const fileSize = (file.size / 1024 / 1024).toFixed(2); // Convert to MB
            fileInfo.innerHTML = `
                <strong>Selected:</strong> ${file.name}<br>
                <strong>Size:</strong> ${fileSize} MB<br>
                <strong>Type:</strong> ${file.type || 'Unknown'}
            `;
            fileInfo.style.color = '#48bb78';
        } else {
            fileInfo.innerHTML = '';
        }
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Show loading state
        setLoadingState(true);
        hideError();
        hideResult();

        try {
            const formData = new FormData(form);

            const response = await fetch('/generate', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                showResult(data.cover_letter);
            } else {
                showError(data.error || 'An error occurred while generating the cover letter');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            setLoadingState(false);
        }
    });

    // Copy to clipboard functionality
    copyBtn.addEventListener('click', async function() {
        try {
            await navigator.clipboard.writeText(coverLetterText.textContent);

            // Show success feedback
            const originalText = copyBtn.querySelector('.btn-text').textContent;
            copyBtn.querySelector('.btn-text').textContent = '✅ Copied!';
            copyBtn.style.background = '#48bb78';

            setTimeout(() => {
                copyBtn.querySelector('.btn-text').textContent = originalText;
                copyBtn.style.background = '';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy: ', err);
            showError('Failed to copy to clipboard. Please select and copy manually.');
        }
    });

    // Generate new letter button
    newLetterBtn.addEventListener('click', function() {
        hideResult();
        form.reset();
        fileInfo.innerHTML = '';
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Utility functions
    function setLoadingState(isLoading) {
        const btnText = generateBtn.querySelector('.btn-text');
        const btnLoading = generateBtn.querySelector('.btn-loading');

        if (isLoading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'flex';
            generateBtn.disabled = true;
        } else {
            btnText.style.display = 'inline';
            btnLoading.style.display = 'none';
            generateBtn.disabled = false;
        }
    }

    function showResult(coverLetter) {
        coverLetterText.textContent = coverLetter;
        resultSection.style.display = 'block';

        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function hideResult() {
        resultSection.style.display = 'none';
    }

    function showError(message) {
        document.getElementById('errorText').textContent = message;
        errorSection.style.display = 'block';

        // Scroll to error
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function hideError() {
        errorSection.style.display = 'none';
    }

    // Drag and drop functionality for file upload
    const fileUploadLabel = document.querySelector('.file-upload-label');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        fileUploadLabel.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        fileUploadLabel.style.borderColor = '#667eea';
        fileUploadLabel.style.background = '#f0f4ff';
    }

    function unhighlight(e) {
        fileUploadLabel.style.borderColor = '#cbd5e0';
        fileUploadLabel.style.background = '#f7fafc';
    }

    fileUploadLabel.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            cvFileInput.files = files;
            cvFileInput.dispatchEvent(new Event('change'));
        }
    }

    // Auto-resize textarea
    const jobDescriptionTextarea = document.getElementById('jobDescription');
    jobDescriptionTextarea.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 300) + 'px';
    });
});
