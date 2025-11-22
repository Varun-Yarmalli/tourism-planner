"""
Tourism AI Agent - Parent Agent
Orchestrates the multi-agent system and coordinates Weather and Places agents
"""
import re
from typing import Dict, Optional, Tuple, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from weather_agent import WeatherAgent
from places_agent import PlacesAgent


class TourismAgent:
    """Parent agent that orchestrates the tourism system"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def extract_place_name(self, user_input: str) -> Optional[str]:
        """
        Extract place name from user input - case-insensitive, handles spelling mistakes
        Supports all cities globally
        
        Args:
            user_input: User's input text
            
        Returns:
            Place name or None if not found
        """
        # Normalize input for better matching
        user_input_lower = user_input.lower()
        
        # Common patterns for place extraction - case-insensitive
        patterns = [
            r"going to go to ([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"going to (?:go to |visit )?([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"visit (?:to )?([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"trip to ([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"in ([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"to ([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
            r"plan.*?([a-zA-Z\s\-']+?)(?:,|\.|$|\?|let|what|and)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                place = match.group(1).strip()
                # Clean up common words and trailing punctuation
                place = re.sub(r'\b(?:the|a|an|my|our|trip|visit|going|go)\b', '', place, flags=re.IGNORECASE).strip()
                place = re.sub(r'[,\\.!?]+$', '', place).strip()
                if place and len(place) > 2:
                    # Capitalize first letter of each word for better matching
                    place = ' '.join(word.capitalize() for word in place.split())
                    return place
        
        # Fallback: extract any significant word/phrase (case-insensitive)
        words = user_input.split()
        significant_words: List[str] = []
        skip_words = {'i', 'im', 'going', 'go', 'to', 'the', 'a', 'an', 'my', 'our', 
                      'trip', 'visit', 'plan', 'lets', 'let', 'what', 'is', 'are', 
                      'there', 'and', 'can', 'i', 'visit', 'places', 'temperature'}
        
        for word in words:
            word_clean = word.strip('.,!?').lower()
            if word_clean not in skip_words and len(word_clean) > 2:
                significant_words.append(word.strip('.,!?'))
        
        if significant_words:
            # Take first 1-3 significant words as place name
            place = ' '.join(significant_words[:3]).title()
            return place
        
        return None
    
    def determine_user_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Determine what the user wants: weather, places, or both
        
        Args:
            user_input: User's input text
            
        Returns:
            Dictionary with 'weather' and 'places' boolean flags
        """
        user_lower = user_input.lower()
        
        wants_weather = any(keyword in user_lower for keyword in [
            'temperature', 'temp', 'weather', 'rain', 'forecast', 'climate'
        ])
        
        wants_places = any(keyword in user_lower for keyword in [
            'places', 'attractions', 'visit', 'see', 'tourist', 'sightseeing', 'go to'
        ])
        
        # If neither is explicitly mentioned, assume both
        if not wants_weather and not wants_places:
            wants_weather = True
            wants_places = True
        
        return {
            'weather': wants_weather,
            'places': wants_places
        }
    
    def get_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a place (delegates to Places Agent)
        
        Args:
            place_name: Name of the place
            
        Returns:
            Tuple of (latitude, longitude) or None if place doesn't exist
        """
        return self.places_agent.get_coordinates(place_name)
    
    def process_request(self, user_input: str) -> str:
        """
        Main method to process user request - optimized for speed with parallel processing
        
        Args:
            user_input: User's input text
            
        Returns:
            Formatted response string
        """
        # Extract place name (case-insensitive)
        place_name = self.extract_place_name(user_input)
        
        if not place_name:
            return "I couldn't identify the place you want to visit. Please specify a place name."
        
        # Get coordinates to verify place exists
        coordinates = self.get_coordinates(place_name)
        
        if not coordinates:
            return f"I don't know this place exists. Could you please check the spelling or provide more details about the location?"
        
        lat, lon = coordinates
        
        # Determine user intent
        intent = self.determine_user_intent(user_input)
        
        # Use parallel processing for faster results
        weather_response = None
        places = None
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {}
            
            # Submit weather request if needed
            if intent['weather']:
                futures['weather'] = executor.submit(self.weather_agent.get_weather, lat, lon)
            
            # Submit places request if needed
            if intent['places']:
                futures['places'] = executor.submit(self.places_agent.get_tourist_places, lat, lon, 5)
            
            # Collect results as they complete
            for key, future in futures.items():
                try:
                    result = future.result(timeout=30)
                    if key == 'weather' and result:
                        weather_response = self.weather_agent.format_weather_response(place_name, result)
                    elif key == 'places' and result:
                        places = result
                except Exception as e:
                    print(f"Error fetching {key}: {e}")
        
        # Format response based on what was requested
        if weather_response and places:
            # Both weather and places
            places_list = "\n".join(places)
            return f"{weather_response}. And these are the places you can go:\n\n{places_list}"
        elif weather_response:
            # Only weather
            return weather_response
        elif places:
            # Only places
            return self.places_agent.format_places_response(place_name, places)
        else:
            return f"I couldn't fetch information for {place_name}. Please try again."

