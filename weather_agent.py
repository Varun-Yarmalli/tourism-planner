"""
Weather Agent - Child Agent 1
Fetches current weather and forecast using Open-Meteo API
"""
import requests
from typing import Dict, Optional, Tuple, Any


class WeatherAgent:
    """Agent responsible for fetching weather information"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
        """
        Get current weather and forecast for given coordinates
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            
        Returns:
            Dictionary with weather information or None if error
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,precipitation_probability",
                "forecast_days": 1
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "current" in data:
                current = data["current"]
                temperature = current.get("temperature_2m")
                precipitation_prob = current.get("precipitation_probability", 0)
                
                # Handle None temperature values
                if temperature is None:
                    temperature = "N/A"
                else:
                    # Ensure temperature is a number
                    try:
                        temperature = float(temperature)
                    except (ValueError, TypeError):
                        temperature = "N/A"
                
                # Ensure precipitation_probability is a number
                try:
                    precipitation_prob = int(precipitation_prob) if precipitation_prob is not None else 0
                except (ValueError, TypeError):
                    precipitation_prob = 0
                
                return {
                    "temperature": temperature,
                    "precipitation_probability": precipitation_prob,
                    "success": True
                }
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Weather API error: {e}")
            return None
    
    def format_weather_response(self, place_name: str, weather_data: Dict[str, Any]) -> str:
        """
        Format weather data into user-friendly response
        
        Args:
            place_name: Name of the place
            weather_data: Weather data dictionary
            
        Returns:
            Formatted string response
        """
        if not weather_data or not weather_data.get("success"):
            return f"Sorry, I couldn't fetch weather information for {place_name}."
        
        temp = weather_data.get("temperature", "N/A")
        rain_chance = weather_data.get("precipitation_probability", 0)
        
        # Format temperature properly
        if isinstance(temp, (int, float)):
            temp_str = f"{int(temp)}"
        else:
            temp_str = str(temp)
        
        return f"In {place_name} it's currently {temp_str}°C with a chance of {rain_chance}% to rain."

