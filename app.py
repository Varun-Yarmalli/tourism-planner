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
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
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
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #4facfe);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 24px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 24px;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(255, 255, 255, 0.5) inset;
            max-width: 840px;
            width: 100%;
            padding: 48px 40px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 32px 24px;
                border-radius: 20px;
            }
        }
        
        h1 {
            color: #1a1a1a;
            margin-bottom: 12px;
            font-size: clamp(2rem, 5vw, 2.75rem);
            font-weight: 700;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            color: #6b7280;
            margin-bottom: 40px;
            font-size: clamp(1rem, 2.5vw, 1.125rem);
            line-height: 1.6;
            font-weight: 400;
        }
        
        .input-group {
            margin-bottom: 24px;
            position: relative;
        }
        
        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }
        
        .input-icon {
            position: absolute;
            left: 18px;
            color: #9ca3af;
            font-size: 20px;
            pointer-events: none;
            transition: color 0.3s ease;
        }
        
        input[type="text"] {
            width: 100%;
            padding: 18px 18px 18px 52px;
            font-size: 16px;
            border: 2px solid #e5e7eb;
            border-radius: 14px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            background: #ffffff;
            color: #1f2937;
            font-weight: 400;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        input[type="text"]::placeholder {
            color: #9ca3af;
            font-weight: 400;
        }
        
        input[type="text"]:hover {
            border-color: #d1d5db;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 
                0 0 0 4px rgba(102, 126, 234, 0.1),
                0 4px 12px rgba(102, 126, 234, 0.15);
            transform: translateY(-1px);
        }
        
        input[type="text"]:focus + .input-icon,
        input[type="text"]:focus ~ .input-icon {
            color: #667eea;
        }
        
        button {
            width: 100%;
            padding: 18px 24px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            background-size: 200% 200%;
            color: white;
            border: none;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 4px 14px rgba(102, 126, 234, 0.4),
                0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 8px 20px rgba(102, 126, 234, 0.5),
                0 4px 8px rgba(0, 0, 0, 0.15);
            background-position: right center;
        }
        
        button:hover::before {
            left: 100%;
        }
        
        button:active {
            transform: translateY(0);
            box-shadow: 
                0 2px 8px rgba(102, 126, 234, 0.4),
                0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            margin-top: 32px;
            padding: 24px;
        }
        
        .loading.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }
        
        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid rgba(102, 126, 234, 0.2);
            border-top-color: #667eea;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 12px;
        }
        
        .loading-text {
            color: #667eea;
            font-size: 15px;
            font-weight: 500;
            margin-top: 8px;
        }
        
        .response {
            margin-top: 32px;
            padding: 0;
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.1),
                0 0 0 1px rgba(102, 126, 234, 0.1) inset;
            min-height: 60px;
            opacity: 0;
            transform: translateY(10px);
            transition: opacity 0.4s ease, transform 0.4s ease;
            overflow: hidden;
        }
        
        .response.show {
            opacity: 1;
            transform: translateY(0);
            animation: fadeIn 0.5s ease;
        }
        
        .response-content {
            padding: 28px;
            white-space: pre-wrap;
            line-height: 1.8;
            color: #1f2937;
            font-size: 15px;
        }
        
        .response-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .weather-icon {
            font-size: 32px;
            line-height: 1;
        }
        
        .response-title {
            font-weight: 600;
            font-size: 18px;
            color: #1f2937;
        }
        
        .places-list {
            margin-top: 20px;
            padding-left: 0;
            list-style: none;
        }
        
        .places-list li {
            padding: 12px 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            color: #374151;
            font-size: 15px;
            position: relative;
            padding-left: 24px;
        }
        
        .places-list li:last-child {
            border-bottom: none;
        }
        
        .places-list li::before {
            content: '📍';
            position: absolute;
            left: 0;
            font-size: 16px;
        }
        
        .more-details {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .details-toggle {
            background: rgba(102, 126, 234, 0.1);
            border: 1px solid rgba(102, 126, 234, 0.2);
            color: #667eea;
            padding: 10px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
            width: 100%;
            text-align: left;
        }
        
        .details-toggle:hover {
            background: rgba(102, 126, 234, 0.15);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .details-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease, padding 0.3s ease;
            padding: 0 16px;
            background: rgba(102, 126, 234, 0.05);
            border-radius: 8px;
            margin-top: 12px;
        }
        
        .details-content.expanded {
            max-height: 500px;
            padding: 16px;
        }
        
        .error {
            border-left: 4px solid #ef4444;
            background: rgba(239, 68, 68, 0.05);
        }
        
        @media (max-width: 768px) {
            body {
                padding: 16px;
            }
            
            h1 {
                margin-bottom: 8px;
            }
            
            .subtitle {
                margin-bottom: 32px;
                font-size: 0.95rem;
            }
            
            input[type="text"] {
                padding: 16px 16px 16px 48px;
                font-size: 16px;
            }
            
            button {
                padding: 16px 20px;
                font-size: 15px;
            }
            
            .response-content {
                padding: 20px;
                font-size: 14px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Tourism AI System</h1>
        <p class="subtitle">Get weather and tourist attraction information for any place</p>
        
        <form id="queryForm">
            <div class="input-group">
                <div class="input-wrapper">
                    <span class="input-icon">🔍</span>
                    <input type="text" id="userInput" name="query" 
                           placeholder="Enter a city name and ask about weather or places to visit" 
                           required>
                </div>
            </div>
            <button type="submit" id="submitBtn">Get Information</button>
        </form>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div class="loading-text">Processing your request...</div>
        </div>
        
        <div class="response" id="response"></div>
    </div>

    <script>
        function getWeatherIcon(text) {
            const lowerText = text.toLowerCase();
            if (lowerText.includes('rain') || lowerText.includes('precipitation')) {
                return '🌧️';
            } else if (lowerText.includes('sun') || lowerText.includes('clear')) {
                return '☀️';
            } else if (lowerText.includes('cloud')) {
                return '☁️';
            } else if (lowerText.includes('snow')) {
                return '❄️';
            } else if (lowerText.includes('storm')) {
                return '⛈️';
            } else if (lowerText.includes('fog') || lowerText.includes('mist')) {
                return '🌫️';
            }
            return '🌤️';
        }
        
        function formatResponse(text) {
            const hasWeather = text.toLowerCase().includes('temperature') || text.toLowerCase().includes('°c');
            const hasPlaces = text.includes('\n') && text.split('\n').length > 2;
            
            let html = '';
            
            if (hasWeather) {
                const weatherIcon = getWeatherIcon(text);
                html += '<div class="response-header">';
                html += `<span class="weather-icon">${weatherIcon}</span>`;
                html += '<span class="response-title">Weather Information</span>';
                html += '</div>';
            }
            
            const parts = text.split('\n\n');
            let mainContent = '';
            let placesList = '';
            
            parts.forEach(part => {
                if (part.includes('°C') || part.includes('temperature')) {
                    mainContent += `<div style="margin-bottom: 16px;">${part}</div>`;
                } else if (part.includes('places you can go')) {
                    mainContent += `<div style="margin-bottom: 12px; font-weight: 500;">${part.split(':')[0]}:</div>`;
                    const places = part.split('\n').slice(1).filter(p => p.trim());
                    if (places.length > 0) {
                        placesList = '<ul class="places-list">';
                        places.forEach(place => {
                            if (place.trim()) {
                                placesList += `<li>${place.trim()}</li>`;
                            }
                        });
                        placesList += '</ul>';
                    }
                } else if (part.trim()) {
                    mainContent += `<div>${part}</div>`;
                }
            });
            
            if (!hasWeather && !mainContent) {
                mainContent = text;
            }
            
            html += '<div class="response-content">';
            html += mainContent;
            if (placesList) {
                html += placesList;
            }
            
            if (hasWeather || hasPlaces) {
                html += '<div class="more-details">';
                html += '<button type="button" class="details-toggle" onclick="toggleDetails(this)">';
                html += '<span>ℹ️ More Details</span>';
                html += '</button>';
                html += '<div class="details-content">';
                html += '<p style="margin: 0; color: #6b7280; font-size: 14px; line-height: 1.6;">';
                html += 'This information is fetched in real-time using open-source APIs. ';
                html += 'Weather data is provided by Open-Meteo, and tourist attractions are sourced from OpenStreetMap.';
                html += '</p>';
                html += '</div>';
                html += '</div>';
            }
            
            html += '</div>';
            return html;
        }
        
        function toggleDetails(button) {
            const content = button.nextElementSibling;
            const isExpanded = content.classList.contains('expanded');
            
            if (isExpanded) {
                content.classList.remove('expanded');
                button.querySelector('span').textContent = 'ℹ️ More Details';
            } else {
                content.classList.add('expanded');
                button.querySelector('span').textContent = 'ℹ️ Less Details';
            }
        }
        
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = document.getElementById('userInput').value;
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            const submitBtn = document.getElementById('submitBtn');
            
            responseDiv.innerHTML = '';
            responseDiv.classList.remove('show', 'error');
            loadingDiv.classList.add('active');
            submitBtn.disabled = true;
            
            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: input })
                });
                
                const data = await response.json();
                loadingDiv.classList.remove('active');
                submitBtn.disabled = false;
                
                if (data.success) {
                    responseDiv.innerHTML = formatResponse(data.response);
                    responseDiv.classList.add('show');
                    setTimeout(() => {
                        responseDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
                } else {
                    responseDiv.innerHTML = `<div class="response-content" style="color: #ef4444;">Error: ${data.error}</div>`;
                    responseDiv.classList.add('show', 'error');
                }
            } catch (error) {
                loadingDiv.classList.remove('active');
                submitBtn.disabled = false;
                responseDiv.innerHTML = `<div class="response-content" style="color: #ef4444;">Error: ${error.message}</div>`;
                responseDiv.classList.add('show', 'error');
            }
        });
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
        user_input = data.get('query', '').strip()
        
        if not user_input:
            return jsonify({
                'success': False,
                'error': 'Please provide a query'
            }), 400
        
        # Process the request using the tourism agent
        response = agent.process_request(user_input)
        
        return jsonify({
            'success': True,
            'response': response
        })
        
    except Exception as e:
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

