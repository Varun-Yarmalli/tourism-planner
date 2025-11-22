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
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
            padding: 40px;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        .input-group {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            font-size: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .response {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            white-space: pre-wrap;
            line-height: 1.6;
            min-height: 50px;
        }
        .loading {
            display: none;
            text-align: center;
            color: #667eea;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 Tourism AI System</h1>
        <p class="subtitle">Get weather and tourist attraction information for any place</p>
        
        <form id="queryForm">
            <div class="input-group">
                <input type="text" id="userInput" name="query" 
                       placeholder="Enter a city name and ask about weather or places to visit" 
                       required>
            </div>
            <button type="submit">Get Information</button>
        </form>
        
        <div class="loading" id="loading">Processing your request...</div>
        
        <div class="response" id="response"></div>
    </div>

    <script>
        document.getElementById('queryForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const input = document.getElementById('userInput').value;
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            
            responseDiv.textContent = '';
            loadingDiv.style.display = 'block';
            
            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: input })
                });
                
                const data = await response.json();
                loadingDiv.style.display = 'none';
                
                if (data.success) {
                    responseDiv.textContent = data.response;
                } else {
                    responseDiv.textContent = 'Error: ' + data.error;
                    responseDiv.style.borderLeftColor = '#e74c3c';
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                responseDiv.textContent = 'Error: ' + error.message;
                responseDiv.style.borderLeftColor = '#e74c3c';
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

