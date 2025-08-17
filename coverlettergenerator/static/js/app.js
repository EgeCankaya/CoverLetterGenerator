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
    const historyBtn = document.getElementById('historyBtn');
    const historySection = document.getElementById('historySection');
    const historyList = document.getElementById('historyList');
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');

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
                // Refresh history if it's currently visible
                if (historySection.style.display !== 'none') {
                    loadHistory();
                }
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

    // History button
    historyBtn.addEventListener('click', function() {
        if (historySection.style.display === 'none') {
            showHistory();
        } else {
            hideHistory();
        }
    });

    // Clear history button
    clearHistoryBtn.addEventListener('click', function() {
        if (confirm('Are you sure you want to clear all history? This action cannot be undone.')) {
            clearHistory();
        }
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

    // History functions
    async function showHistory() {
        hideResult();
        hideError();
        historySection.style.display = 'block';
        await loadHistory();
        historySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    function hideHistory() {
        historySection.style.display = 'none';
    }

    async function loadHistory() {
        try {
            const response = await fetch('/history');
            const data = await response.json();

            if (response.ok) {
                displayHistory(data.history);
            } else {
                showError(data.error || 'Failed to load history');
            }
        } catch (error) {
            console.error('Error loading history:', error);
            showError('Network error while loading history');
        }
    }

    function displayHistory(history) {
        if (history.length === 0) {
            historyList.innerHTML = '<p style="text-align: center; color: #718096; font-style: italic;">No history found. Generate your first cover letter to see it here!</p>';
            return;
        }

        historyList.innerHTML = history.map(item => `
            <div class="history-item">
                <div class="history-item-header">
                    <div>
                        <div class="history-item-title">${escapeHtml(item.company_name)}</div>
                        <div class="history-item-cv">CV: ${escapeHtml(item.cv_filename)}</div>
                    </div>
                    <div class="history-item-date">${formatDate(item.created_at)}</div>
                </div>
                <div class="history-item-preview">${escapeHtml(item.generated_cover_letter.substring(0, 300))}${item.generated_cover_letter.length > 300 ? '...' : ''}</div>
                <div class="history-item-actions">
                    <button class="btn btn-outline" onclick="viewFullCoverLetter(${item.id})">👁️ View Full</button>
                    <button class="btn btn-secondary" onclick="copyCoverLetter(${item.id})">📋 Copy</button>
                </div>
            </div>
        `).join('');
    }

    async function clearHistory() {
        try {
            const response = await fetch('/history/clear', {
                method: 'DELETE'
            });
            const data = await response.json();

            if (response.ok) {
                historyList.innerHTML = '<p style="text-align: center; color: #718096; font-style: italic;">No history found. Generate your first cover letter to see it here!</p>';
                showSuccessMessage('History cleared successfully');
            } else {
                showError(data.error || 'Failed to clear history');
            }
        } catch (error) {
            console.error('Error clearing history:', error);
            showError('Network error while clearing history');
        }
    }

    // Global functions for history actions
    window.viewFullCoverLetter = async function(historyId) {
        try {
            const response = await fetch(`/history/${historyId}`);
            const data = await response.json();

            if (response.ok) {
                showResult(data.generated_cover_letter);
                hideHistory();
            } else {
                showError(data.error || 'Failed to load cover letter');
            }
        } catch (error) {
            console.error('Error loading cover letter:', error);
            showError('Network error while loading cover letter');
        }
    };

    window.copyCoverLetter = async function(historyId) {
        try {
            const response = await fetch(`/history/${historyId}`);
            const data = await response.json();

            if (response.ok) {
                await navigator.clipboard.writeText(data.generated_cover_letter);
                showSuccessMessage('Cover letter copied to clipboard!');
            } else {
                showError(data.error || 'Failed to load cover letter');
            }
        } catch (error) {
            console.error('Error copying cover letter:', error);
            showError('Failed to copy cover letter');
        }
    };

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function showSuccessMessage(message) {
        // Create a temporary success message
        const successDiv = document.createElement('div');
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #48bb78;
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            font-weight: 500;
        `;
        successDiv.textContent = message;
        document.body.appendChild(successDiv);

        setTimeout(() => {
            successDiv.remove();
        }, 3000);
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
