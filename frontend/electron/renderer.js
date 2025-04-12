const API_BASE_URL = 'http://localhost:8000';

async function fetchFromAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Error fetching from API:', error);
        throw error;
    }
}

// API functions
async function uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/upload_resume`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

async function getQuestions() {
    return await fetchFromAPI('/get_questions');
}

async function submitAnswer(questionId, answer) {
    return await fetchFromAPI('/submit_answer', {
        method: 'POST',
        body: JSON.stringify({
            question_id: questionId,
            answer: answer,
        }),
    });
}

// Export functions for use in the frontend
window.api = {
    uploadResume,
    getQuestions,
    submitAnswer,
};