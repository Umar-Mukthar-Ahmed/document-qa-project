// Main application JavaScript

let chatMessages = document.getElementById('chat-messages');
let questionInput = document.getElementById('question-input');
let askButton = document.getElementById('ask-button');

// Handle Enter key (Shift+Enter for new line)
questionInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        askQuestion();
    }
});

// Example questions click handler
document.querySelectorAll('.example-questions li').forEach((li) => {
    li.addEventListener('click', () => {
        questionInput.value = li.textContent;
        askQuestion();
    });
});

async function askQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        alert('Please enter a question');
        return;
    }

    // Disable input while processing
    questionInput.disabled = true;
    askButton.disabled = true;
    document.getElementById('button-text').style.display = 'none';
    document.getElementById('button-loading').style.display = 'inline';

    // Add user message to chat
    addMessage(question, 'user');

    // Clear input
    questionInput.value = '';

    try {
        // Call API
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (response.ok) {
            // Add assistant response
            addMessage(data.answer, 'assistant', data.sources);
        } else {
            addMessage(`Error: ${data.error}`, 'assistant');
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'assistant');
    } finally {
        // Re-enable input
        questionInput.disabled = false;
        askButton.disabled = false;
        document.getElementById('button-text').style.display = 'inline';
        document.getElementById('button-loading').style.display = 'none';
        questionInput.focus();
    }
}

function addMessage(text, type, sources = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;

    let html = `<div class="message-text">${text}</div>`;

    if (sources && sources.length > 0) {
        html += `<div class="sources">📚 Sources: ${sources.join(', ')}</div>`;
    }

    messageDiv.innerHTML = html;
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Update stats periodically
async function updateStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();

        if (response.ok) {
            document.getElementById('doc-count').textContent =
                `Documents indexed: ${data.document_count}`;
        }
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

// Update stats every 30 seconds
setInterval(updateStats, 30000);
