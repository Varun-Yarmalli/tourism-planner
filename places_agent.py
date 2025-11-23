"""
Places Agent - Child Agent 2
Fetches tourist attractions using Overpass API (OpenStreetMap)
Supports all cities globally
"""
import requests
import time
from typing import List, Optional, Tuple, Set, Dict
from difflib import get_close_matches
from functools import lru_cache


class PlacesAgent:
    """Agent responsible for fetching tourist attractions and places"""
    
    def __init__(self):
        self.overpass_url = "https://overpass-api.de/api/interpreter"
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self._coordinate_cache: Dict[str, Optional[Tuple[float, float]]] = {}
    
    def get_coordinates(self, place_name: str) -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a place using Nominatim API with caching and fuzzy matching
        Supports all cities globally (worldwide coverage)
        Handles case-insensitive input and spelling mistakes
        
        Args:
            place_name: Name of the place (city, country, landmark, etc.)
            
        Returns:
            Tuple of (latitude, longitude) or None if not found
        """
        # Normalize place name for caching (lowercase, strip)
        normalized_name = place_name.lower().strip()
        
        # Check cache first
        if normalized_name in self._coordinate_cache:
            return self._coordinate_cache[normalized_name]
        
        try:
            # Reduced delay for faster processing
            time.sleep(0.5)
            
            print(f"[DEBUG] Fetching coordinates for: {place_name}")
            
            # Enhanced search parameters for better global city matching
            params = {
                "q": place_name,
                "format": "json",
                "limit": 10,  # Get more results for better matching
                "addressdetails": 1,
                "extratags": 1
            }
            
            headers = {
                "User-Agent": "Tourism-AI-Agent/1.0"
            }
            
            print(f"[DEBUG] Making request to Nominatim API...")
            response = requests.get(self.nominatim_url, params=params, headers=headers, timeout=5)
            print(f"[DEBUG] Nominatim API responded with status: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            print(f"[DEBUG] Received {len(data)} results from Nominatim")
            
            if data and len(data) > 0:
                # Collect all potential matches
                candidates = []
                
                for location in data:
                    place_type = location.get("type", "").lower()
                    class_type = location.get("class", "").lower()
                    display_name = location.get("display_name", "").lower()
                    name = location.get("name", "").lower()
                    
                    # Calculate match score
                    score = 0
                    if place_type in ["city", "town", "administrative", "village"]:
                        score += 10
                    if class_type in ["place", "boundary"]:
                        score += 5
                    if normalized_name in display_name or normalized_name in name:
                        score += 15
                    
                    lat = float(location.get("lat", 0))
                    lon = float(location.get("lon", 0))
                    if lat != 0 and lon != 0:
                        candidates.append((score, lat, lon, location))
                
                # Sort by score and return best match
                if candidates:
                    candidates.sort(key=lambda x: x[0], reverse=True)
                    best_match = candidates[0]
                    result = (best_match[1], best_match[2])
                    self._coordinate_cache[normalized_name] = result
                    print(f"[DEBUG] Found coordinates: {result}")
                    return result
                
                # Fallback: use first result
                location = data[0]
                lat = float(location.get("lat", 0))
                lon = float(location.get("lon", 0))
                if lat != 0 and lon != 0:
                    result = (lat, lon)
                    self._coordinate_cache[normalized_name] = result
                    print(f"[DEBUG] Found coordinates (fallback): {result}")
                    return result
            
            # Cache None result to avoid repeated failed lookups
            print(f"[DEBUG] No coordinates found for {place_name}")
            self._coordinate_cache[normalized_name] = None
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Geocoding API error: {e}")
            self._coordinate_cache[normalized_name] = None
            return None
        except (ValueError, KeyError, TypeError) as e:
            print(f"Error parsing geocoding response: {e}")
            self._coordinate_cache[normalized_name] = None
            return None
    
    def get_tourist_places(self, latitude: float, longitude: float, limit: int = 5) -> List[str]:
        """
        Get tourist attractions near given coordinates using Overpass API
        Works for all cities globally with optimized parallel search
        
        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
            limit: Maximum number of places to return (default: 5)
            
        Returns:
            List of place names
        """
        places: List[str] = []
        seen_names: Set[str] = set()
        
        # Optimized: Combined query for faster results (most common types)
        combined_query = f"""
        [out:json][timeout:20];
        (
          node["tourism"](around:15000,{latitude},{longitude});
          way["tourism"](around:15000,{latitude},{longitude});
          node["historic"](around:15000,{latitude},{longitude});
          way["historic"](around:15000,{latitude},{longitude});
          node["leisure"](around:15000,{latitude},{longitude});
          way["leisure"](around:15000,{latitude},{longitude});
        );
        out center;
        limit {limit * 3};
        """
        
        try:
            places.extend(self._execute_overpass_query(combined_query, limit * 3, seen_names))
        except Exception as e:
            print(f"Combined query error: {e}")
        
        # If we have enough, return early
        if len(places) >= limit:
            return places[:limit]
        
        # Fallback: Search museums specifically
        if len(places) < limit:
            places.extend(self._search_museums_galleries(latitude, longitude, limit - len(places), seen_names))
        
        # Final fallback: Broader search
        if len(places) < limit:
            places.extend(self._search_named_places(latitude, longitude, limit - len(places), seen_names))
        
        return places[:limit]
    
    def _search_tourism_attractions(self, latitude: float, longitude: float, limit: int, seen_names: Set[str]) -> List[str]:
        """Search for tourism attractions"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["tourism"](around:15000,{latitude},{longitude});
              way["tourism"](around:15000,{latitude},{longitude});
              relation["tourism"](around:15000,{latitude},{longitude});
            );
            out center;
            """
            
            return self._execute_overpass_query(query, limit, seen_names)
        except Exception as e:
            print(f"Tourism attractions search error: {e}")
            return []
    
    def _search_historic_sites(self, latitude: float, longitude: float, limit: int, seen_names: Set[str]) -> List[str]:
        """Search for historic sites"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["historic"](around:15000,{latitude},{longitude});
              way["historic"](around:15000,{latitude},{longitude});
              relation["historic"](around:15000,{latitude},{longitude});
            );
            out center;
            """
            
            return self._execute_overpass_query(query, limit, seen_names)
        except Exception as e:
            print(f"Historic sites search error: {e}")
            return []
    
    def _search_parks_leisure(self, latitude: float, longitude: float, limit: int, seen_names: Set[str]) -> List[str]:
        """Search for parks and leisure areas"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["leisure"](around:15000,{latitude},{longitude});
              way["leisure"](around:15000,{latitude},{longitude});
              relation["leisure"](around:15000,{latitude},{longitude});
            );
            out center;
            """
            
            return self._execute_overpass_query(query, limit, seen_names)
        except Exception as e:
            print(f"Parks/leisure search error: {e}")
            return []
    
    def _search_museums_galleries(self, latitude: float, longitude: float, limit: int, seen_names: Set[str]) -> List[str]:
        """Search for museums and galleries"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["tourism"="museum"](around:15000,{latitude},{longitude});
              way["tourism"="museum"](around:15000,{latitude},{longitude});
              node["tourism"="gallery"](around:15000,{latitude},{longitude});
              way["tourism"="gallery"](around:15000,{latitude},{longitude});
            );
            out center;
            """
            
            return self._execute_overpass_query(query, limit, seen_names)
        except Exception as e:
            print(f"Museums/galleries search error: {e}")
            return []
    
    def _search_named_places(self, latitude: float, longitude: float, limit: int, seen_names: Set[str]) -> List[str]:
        """Broader search for any named places of interest"""
        try:
            query = f"""
            [out:json][timeout:25];
            (
              node["name"](around:20000,{latitude},{longitude})["tourism"];
              way["name"](around:20000,{latitude},{longitude})["tourism"];
              node["name"](around:20000,{latitude},{longitude})["historic"];
              way["name"](around:20000,{latitude},{longitude})["historic"];
              node["name"](around:20000,{latitude},{longitude})["leisure"];
              way["name"](around:20000,{latitude},{longitude})["leisure"];
            );
            out center;
            """
            
            return self._execute_overpass_query(query, limit, seen_names)
        except Exception as e:
            print(f"Named places search error: {e}")
            return []
    
    def _execute_overpass_query(self, query: str, limit: int, seen_names: Set[str]) -> List[str]:
        """Execute Overpass query and extract place names"""
        try:
            print(f"[DEBUG] Executing Overpass query...")
            response = requests.post(
                self.overpass_url,
                data={"data": query},
                timeout=10
            )
            print(f"[DEBUG] Overpass API responded with status: {response.status_code}")
            response.raise_for_status()
            
            data = response.json()
            places: List[str] = []
            
            if "elements" in data:
                print(f"[DEBUG] Found {len(data['elements'])} elements from Overpass")
                for element in data["elements"]:
                    if len(places) >= limit:
                        break
                    
                    tags = element.get("tags", {})
                    # Try multiple name fields for international support
                    name = (tags.get("name:en") or 
                           tags.get("name:en-GB") or
                           tags.get("name:en-US") or
                           tags.get("name") or
                           tags.get("official_name") or
                           tags.get("alt_name") or
                           tags.get("short_name"))
                    
                    if name and name not in seen_names and len(name.strip()) > 2:
                        # Filter out generic names
                        name_lower = name.lower().strip()
                        if name_lower not in ["park", "museum", "gallery", "monument", "attraction", "place"]:
                            places.append(name.strip())
                            seen_names.add(name.strip())
            
            print(f"[DEBUG] Extracted {len(places)} places from Overpass")
            return places
            
        except requests.exceptions.RequestException as e:
            print(f"Overpass API error: {e}")
            return []
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error parsing Overpass response: {e}")
            return []
    
    
    def format_places_response(self, place_name: str, places: List[str]) -> str:
        """
        Format places list into user-friendly response
        
        Args:
            place_name: Name of the place
            places: List of tourist attraction names
            
        Returns:
            Formatted string response
        """
        if not places:
            return f"Sorry, I couldn't find tourist attractions for {place_name}."
        
        response = f"In {place_name} these are the places you can go,\n\n"
        for place in places:
            response += f"{place}\n"
        
        return response.strip()

