# Multi-Agent Tourism System 🌍

A fast, intelligent multi-agent system that helps users plan their trips by providing weather information and tourist attraction suggestions for any city worldwide.

## 🚀 Features

- ✅ **Fast Processing**: Parallel API calls and intelligent caching for quick responses
- ✅ **Case-Insensitive**: Works with any capitalization (bangalore, BANGALORE, Bangalore)
- ✅ **Spelling Tolerance**: Handles minor spelling mistakes intelligently
- ✅ **Global Coverage**: Supports all cities worldwide
- ✅ **Weather Information**: Current temperature and precipitation probability
- ✅ **Tourist Attractions**: Up to 5 curated places to visit
- ✅ **Smart Error Handling**: Graceful handling of non-existent places
- ✅ **Natural Language Processing**: Understands various query formats
- ✅ **No API Keys Required**: Uses open-source APIs

## 🏗️ Architecture

- **Parent Agent**: Tourism AI Agent (`tourism_agent.py`) - Orchestrates the entire system
- **Child Agent 1**: Weather Agent (`weather_agent.py`) - Fetches weather data using Open-Meteo API
- **Child Agent 2**: Places Agent (`places_agent.py`) - Fetches tourist attractions using Overpass API

## APIs Used

1. **Open-Meteo API** - Weather data
   - Endpoint: https://api.open-meteo.com/v1/forecast
   
2. **Nominatim API** - Geocoding (place name to coordinates)
   - Endpoint: https://nominatim.openstreetmap.org/search
   
3. **Overpass API** - Tourist attractions (OpenStreetMap data)
   - Endpoint: https://overpass-api.de/api/interpreter

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-tourism-system.git
cd multi-agent-tourism-system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### Local Development

Run the Flask web server:
```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

### Command Line Interface

Run the CLI version:
```bash
python main.py
```

### Example Queries

1. **Places only:**
   ```
   I'm going to go to Bangalore, let's plan my trip.
   ```

2. **Weather only:**
   ```
   I'm going to go to Bangalore, what is the temperature there
   ```

3. **Both weather and places:**
   ```
   I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?
   ```

## How It Works

1. User enters a query with a place name
2. Parent Agent extracts the place name and determines user intent (weather, places, or both)
3. Parent Agent uses Nominatim API to get coordinates (validates place exists)
4. If place doesn't exist, returns error message
5. If weather requested, Weather Agent fetches data from Open-Meteo API
6. If places requested, Places Agent fetches attractions from Overpass API
7. Parent Agent formats and returns the combined response

## 🌐 Deployment

### Deploy to Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Deploy: `git push heroku main`

### Deploy to Railway

1. Connect your GitHub repository to Railway
2. Railway will auto-detect Python and deploy
3. Set PORT environment variable (auto-set by Railway)

### Deploy to Render

1. Connect your GitHub repository to Render
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`

## 🔧 Performance Optimizations

- **Parallel Processing**: Weather and places fetched simultaneously
- **Coordinate Caching**: Repeated queries are instant
- **Optimized Queries**: Combined API calls for faster results
- **Smart Matching**: Fuzzy matching handles spelling mistakes

## 📝 Example Queries

Try these (all work with any capitalization):

- `im going to bangalore` (lowercase)
- `I'm going to go to Paris` (mixed case)
- `visit tokyo` (simple)
- `trip to new york` (any format)
- `going to london, what is the temperature there?`

## 🛠️ Error Handling

- Non-existent places: Returns "I don't know this place exists..."
- API failures: Gracefully handles errors and provides user-friendly messages
- Invalid input: Prompts user to provide valid place names

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

