"""
Flask Web Server for Multi-Agent Tourism System
"""
from flask import Flask, request, jsonify, render_template_string
from tourism_agent import TourismAgent

app = Flask(__name__)
agent = TourismAgent()

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multi-Agent Tourism System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: #f3f4f6;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
            transition: background 0.3s ease, color 0.3s ease;
        }
        body.dark-mode {
            background: #1a1a1a;
            color: #e5e7eb;
        }
        .container {
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            max-width: 720px;
            width: 100%;
            padding: 48px 40px;
            transition: all 0.3s ease;
        }
        body.dark-mode .container {
            background: #2d2d2d;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 12px;
            font-size: 2.2em;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        body.dark-mode h1 {
            color: #e5e7eb;
        }
        .subtitle {
            color: #7f8c8d;
            margin-bottom: 32px;
            font-size: 1em;
            font-weight: 400;
        }
        body.dark-mode .subtitle {
            color: #9ca3af;
        }
        .theme-toggle {
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 8px 12px;
            cursor: pointer;
            font-size: 20px;
            transition: all 0.2s ease;
        }
        .theme-toggle:hover {
            background: #e5e7eb;
        }
        body.dark-mode .theme-toggle {
            background: #3d3d3d;
            border-color: #4d4d4d;
            color: #e5e7eb;
        }
        .input-group {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 16px;
            font-size: 15px;
            border: 1.5px solid #d1d5db;
            border-radius: 8px;
            transition: all 0.2s ease;
            background: #fafafa;
        }
        body.dark-mode input[type="text"] {
            background: #3d3d3d;
            border-color: #4d4d4d;
            color: #e5e7eb;
        }
        input[type="text"]:hover {
            border-color: #9ca3af;
            background: #ffffff;
        }
        body.dark-mode input[type="text"]:hover {
            background: #4d4d4d;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            background: #ffffff;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        body.dark-mode input[type="text"]:focus {
            background: #4d4d4d;
        }
        button {
            width: 100%;
            padding: 14px 20px;
            font-size: 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(102, 126, 234, 0.2);
        }
        button:hover {
            background: #5568d3;
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
            transform: translateY(-1px);
        }
        button:active {
            transform: translateY(0);
            box-shadow: 0 1px 2px rgba(102, 126, 234, 0.2);
        }
        .response {
            margin-top: 28px;
            padding: 24px;
            background: #f9fafb;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            white-space: pre-wrap;
            line-height: 1.7;
            min-height: 50px;
            color: #374151;
            font-size: 15px;
            position: relative;
        }
        body.dark-mode .response {
            background: #3d3d3d;
            border-color: #4d4d4d;
            color: #e5e7eb;
        }
        .response-actions {
            position: absolute;
            top: 12px;
            right: 12px;
            display: flex;
            gap: 8px;
        }
        .action-btn {
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 6px 10px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .action-btn:hover {
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        body.dark-mode .action-btn {
            background: #4d4d4d;
            border-color: #5d5d5d;
            color: #e5e7eb;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 24px;
            font-size: 14px;
            font-weight: 500;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 12px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .search-history {
            position: relative;
            margin-top: 8px;
        }
        .history-dropdown {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            margin-top: 4px;
            max-height: 200px;
            overflow-y: auto;
            display: none;
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        body.dark-mode .history-dropdown {
            background: #2d2d2d;
            border-color: #4d4d4d;
        }
        .history-item {
            padding: 12px 16px;
            cursor: pointer;
            border-bottom: 1px solid #f3f4f6;
            transition: background 0.2s ease;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .history-item:hover {
            background: #f9fafb;
        }
        body.dark-mode .history-item {
            border-color: #3d3d3d;
        }
        body.dark-mode .history-item:hover {
            background: #3d3d3d;
        }
        .history-item:last-child {
            border-bottom: none;
        }
        .clear-history {
            padding: 8px 16px;
            text-align: center;
            color: #ef4444;
            cursor: pointer;
            font-size: 13px;
            border-top: 1px solid #f3f4f6;
        }
        body.dark-mode .clear-history {
            border-color: #3d3d3d;
        }
        .quick-actions {
            display: flex;
            gap: 8px;
            margin-top: 12px;
            flex-wrap: wrap;
        }
        .quick-btn {
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 6px 12px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s ease;
        }
        .quick-btn:hover {
            background: #e5e7eb;
            transform: translateY(-1px);
        }
        body.dark-mode .quick-btn {
            background: #3d3d3d;
            border-color: #4d4d4d;
            color: #e5e7eb;
        }
        body.dark-mode .quick-btn:hover {
            background: #4d4d4d;
        }
        .char-counter {
            text-align: right;
            font-size: 12px;
            color: #9ca3af;
            margin-top: 4px;
        }
        .fade-in {
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .weather-icon {
            font-size: 2em;
            display: inline-block;
            margin-right: 8px;
        }
        .toast {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: #2c3e50;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            display: none;
            z-index: 1000;
        }
        .toast.show {
            display: block;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @media (max-width: 768px) {
            .response-actions {
                position: static;
                margin-top: 12px;
                justify-content: flex-start;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>Tourism Planner</h1>
                <p class="subtitle">Find weather and attractions for your destination</p>
            </div>
            <button class="theme-toggle" id="themeToggle" title="Toggle dark mode">🌙</button>
        </div>
        
        <form id="queryForm">
            <div class="input-group">
                <input type="text" id="userInput" name="query" 
                       placeholder="Enter a city name and ask about weather or places to visit" 
                       maxlength="200"
                       required>
                <div class="char-counter" id="charCounter">0 / 200</div>
            </div>
            
            <div class="quick-actions">
                <div class="quick-btn" onclick="quickSearch('Paris')">🗼 Paris</div>
                <div class="quick-btn" onclick="quickSearch('Tokyo')">🗾 Tokyo</div>
                <div class="quick-btn" onclick="quickSearch('New York')">🗽 New York</div>
                <div class="quick-btn" onclick="quickSearch('London')">🏰 London</div>
                <div class="quick-btn" onclick="quickSearch('Dubai')">🏜️ Dubai</div>
            </div>
            
            <div class="search-history">
                <div class="history-dropdown" id="historyDropdown"></div>
            </div>
            
            <button type="submit">Get Information</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div>Processing your request...</div>
        </div>
        
        <div class="response" id="response"></div>
    </div>
    
    <div class="toast" id="toast"></div>

    <script>
        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        const body = document.body;
        const userInput = document.getElementById('userInput');
        const charCounter = document.getElementById('charCounter');
        const historyDropdown = document.getElementById('historyDropdown');
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            body.classList.add('dark-mode');
            themeToggle.textContent = '☀️';
        }
        
        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            themeToggle.textContent = isDark ? '☀️' : '🌙';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
        
        // Character counter
        userInput.addEventListener('input', (e) => {
            const length = e.target.value.length;
            charCounter.textContent = `${length} / 200`;
            if (length > 180) {
                charCounter.style.color = '#ef4444';
            } else {
                charCounter.style.color = '#9ca3af';
            }
        });
        
        // Search history management
        function getSearchHistory() {
            const history = localStorage.getItem('searchHistory');
            return history ? JSON.parse(history) : [];
        }
        
        function saveToHistory(query) {
            let history = getSearchHistory();
            history = history.filter(item => item.toLowerCase() !== query.toLowerCase());
            history.unshift(query);
            history = history.slice(0, 5); // Keep last 5
            localStorage.setItem('searchHistory', JSON.stringify(history));
            displayHistory();
        }
        
        function displayHistory() {
            const history = getSearchHistory();
            if (history.length === 0) {
                historyDropdown.style.display = 'none';
                return;
            }
            
            historyDropdown.innerHTML = history.map(item => 
                `<div class="history-item" onmousedown="selectHistory('${item.replace(/'/g, "\\'")}')">
                    <span>🕐 ${item}</span>
                </div>`
            ).join('') + 
            `<div class="clear-history" onmousedown="clearHistory()">Clear History</div>`;
        }
        
        function selectHistory(query) {
            userInput.value = query;
            historyDropdown.style.display = 'none';
            document.getElementById('queryForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
        
        function clearHistory() {
            localStorage.removeItem('searchHistory');
            historyDropdown.style.display = 'none';
        }
        
        // Show history on focus
        userInput.addEventListener('focus', () => {
            displayHistory();
            if (getSearchHistory().length > 0) {
                historyDropdown.style.display = 'block';
            }
        });
        
        userInput.addEventListener('blur', () => {
            setTimeout(() => {
                historyDropdown.style.display = 'none';
            }, 200);
        });
        
        // Quick search
        function quickSearch(city) {
            userInput.value = `I'm going to ${city}, what is the temperature there? And what are the places I can visit?`;
            document.getElementById('queryForm').dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
        }
        
        // Get weather icon based on temperature
        function getWeatherIcon(temp) {
            if (temp >= 30) return '☀️';
            if (temp >= 20) return '🌤️';
            if (temp >= 10) return '⛅';
            if (temp >= 0) return '🌥️';
            return '❄️';
        }
        
        // Toast notification
        function showToast(message) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2000);
        }
        
        // Copy to clipboard
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('✅ Copied to clipboard!');
            }).catch(() => {
                showToast('❌ Failed to copy');
            });
        }
        
        // Share functionality
        function shareResults(text) {
            if (navigator.share) {
                navigator.share({
                    title: 'Tourism Information',
                    text: text
                }).catch(() => showToast('Share cancelled'));
            } else {
                copyToClipboard(text);
            }
        }
        
        // Export as text
        function exportResults(text) {
            const blob = new Blob([text], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `tourism-info-${new Date().toISOString().split('T')[0]}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('📥 File downloaded!');
        }
        
        // Form submission
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = userInput.value.trim();
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            
            if (!input) return;
            
            // Save to history
            saveToHistory(input);
            
            responseDiv.textContent = '';
            responseDiv.classList.remove('fade-in');
            loadingDiv.style.display = 'block';
            
            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: input })
                });
                
                if (!response.ok) {
                    throw new Error(`Server error: ${response.status}`);
                }
                
                const data = await response.json();
                loadingDiv.style.display = 'none';
                
                if (data.success && data.response) {
                    const responseText = data.response;
                    
                    // Extract temperature for weather icon
                    let weatherIcon = '';
                    const tempMatch = responseText.match(/(\d+)°C/);
                    if (tempMatch) {
                        const temp = parseInt(tempMatch[1]);
                        weatherIcon = `<span class="weather-icon">${getWeatherIcon(temp)}</span>`;
                    }
                    
                    responseDiv.innerHTML = `
                        <div class="response-actions">
                            <div class="action-btn" onclick="copyToClipboard(\`${responseText.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)">
                                📋 Copy
                            </div>
                            <div class="action-btn" onclick="shareResults(\`${responseText.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)">
                                🔗 Share
                            </div>
                            <div class="action-btn" onclick="exportResults(\`${responseText.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`)">
                                💾 Export
                            </div>
                        </div>
                        <div style="padding-right: 120px;">${weatherIcon}${escapeHtml(responseText)}</div>
                    `;
                    responseDiv.classList.add('fade-in');
                } else {
                    const errorMsg = data.error || 'No response received from server';
                    responseDiv.textContent = '❌ Error: ' + errorMsg;
                    responseDiv.style.borderLeftColor = '#ef4444';
                    responseDiv.classList.add('fade-in');
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                const errorMsg = error.message || 'Network error occurred';
                responseDiv.textContent = '❌ Error: ' + errorMsg;
                responseDiv.style.borderLeftColor = '#e74c3c';
                responseDiv.classList.add('fade-in');
            }
        });
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Load history on page load
        displayHistory();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/query', methods=['POST'])
def query():
    """Handle API queries"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid request data'
            }), 400
            
        user_input = data.get('query', '').strip()
        
        if not user_input:
            return jsonify({
                'success': False,
                'error': 'Please provide a query'
            }), 400
        
        # Process the request using the tourism agent
        response = agent.process_request(user_input)
        
        if not response:
            return jsonify({
                'success': False,
                'error': 'No response generated'
            }), 500
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in query endpoint: {error_trace}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("Starting Multi-Agent Tourism System Server...")
    print("="*60)
    print(f"\nServer will be available at: http://localhost:{port}")
    print("Press Ctrl+C to stop the server\n")
    app.run(host='0.0.0.0', port=port, debug=False)

