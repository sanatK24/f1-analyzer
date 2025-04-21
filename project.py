import requests
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import webbrowser
import os
import tempfile

@dataclass
class Driver:
    driver_number: int
    first_name: str
    last_name: str
    team_name: str
    team_colour: str
    country_code: str
    headshot_url: str

class F1DriverAPI:
    BASE_URL = "https://api.openf1.org/v1"

    def __init__(self):
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: dict = None) -> Optional[Dict]:
        """Helper method to make API requests with error handling."""
        try:
            response = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {endpoint}: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            return None

    def search_drivers_by_name(self, name: str) -> List[Driver]:
        """
        Search for drivers by name (case-insensitive).
        
        Args:
            name: The name to search for (can be first or last name)
            
        Returns:
            List of matching Driver objects
        """
        # Get all drivers from the latest session
        params = {
            'session_key': 'latest'
        }
        data = self._make_request('drivers', params)
        
        if not data:
            print("Error fetching driver list")
            return []
            
        try:
            drivers = []
            for driver_data in data:
                # Check if name matches
                if (name.lower() in driver_data.get('first_name', '').lower() or 
                    name.lower() in driver_data.get('last_name', '').lower()):
                    drivers.append(Driver(
                        driver_number=driver_data.get('driver_number'),
                        first_name=driver_data.get('first_name', ''),
                        last_name=driver_data.get('last_name', ''),
                        team_name=driver_data.get('team_name', ''),
                        team_colour=driver_data.get('team_colour', ''),
                        country_code=driver_data.get('country_code', ''),
                        headshot_url=driver_data.get('headshot_url', '')
                    ))
            
            return drivers
            
        except (AttributeError, TypeError) as e:
            print(f"Error parsing driver data: {str(e)}")
            return []

    def get_driver_lap_times(self, driver_number: int, session_key: str) -> List[Dict]:
        """
        Get lap times for a specific driver in a session.
        
        Args:
            driver_number: The driver's unique number
            session_key: The session identifier
            
        Returns:
            List of lap times with additional information
        """
        params = {
            'session_key': session_key,
            'driver_number': driver_number
        }
        data = self._make_request('laps', params)
        
        if not data:
            return []
            
        try:
            lap_times = []
            for lap in data:
                lap_times.append({
                    'lap_number': lap.get('lap_number'),
                    'lap_time': lap.get('lap_time'),
                    'sector_1': lap.get('sector_1'),
                    'sector_2': lap.get('sector_2'),
                    'sector_3': lap.get('sector_3'),
                    'compound': lap.get('compound'),
                    'lap_position': lap.get('position')
                })
            return lap_times
            
        except (AttributeError, TypeError) as e:
            print(f"Error parsing lap times: {str(e)}")
            return []

    def get_weather_conditions(self, session_key: str) -> Optional[Dict]:
        """
        Get weather conditions for a specific session.
        
        Args:
            session_key: The session identifier
            
        Returns:
            Dictionary containing weather information
        """
        params = {
            'session_key': session_key
        }
        data = self._make_request('weather', params)
        
        if not data:
            return None
            
        try:
            return {
                'air_temperature': data.get('air_temperature'),
                'track_temperature': data.get('track_temperature'),
                'humidity': data.get('humidity'),
                'wind_speed': data.get('wind_speed'),
                'wind_direction': data.get('wind_direction'),
                'rain_probability': data.get('rain_probability'),
                'weather_status': data.get('weather_status')
            }
            
        except (AttributeError, TypeError) as e:
            print(f"Error parsing weather data: {str(e)}")
            return None

    def get_team_radio(self, driver_number: int, session_key: str) -> List[Dict]:
        """
        Get team radio communications for a specific driver in a session.
        
        Args:
            driver_number: The driver's unique number
            session_key: The session identifier
            
        Returns:
            List of radio communications
        """
        params = {
            'session_key': session_key,
            'driver_number': driver_number
        }
        data = self._make_request('team_radio', params)
        
        if not data:
            return []
            
        try:
            communications = []
            for message in data:
                communications.append({
                    'timestamp': message.get('timestamp'),
                    'direction': message.get('direction'),
                    'message': message.get('message'),
                    'sender': message.get('sender'),
                    'receiver': message.get('receiver')
                })
            return communications
            
        except (AttributeError, TypeError) as e:
            print(f"Error parsing team radio data: {str(e)}")
            return []

def create_html(driver: Driver, details: Dict = None, results: List[Dict] = None, standings: Dict = None, lap_times: List[Dict] = None, weather: Dict = None, team_radio: List[Dict] = None) -> str:
    """Create HTML content for displaying driver information."""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>F1 Driver Information - {driver.first_name} {driver.last_name}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .driver-card {{
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .driver-info {{
                display: flex;
                gap: 20px;
                align-items: center;
            }}
            .driver-image {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
            }}
            .team-badge {{
                display: inline-block;
                padding: 5px 10px;
                border-radius: 20px;
                background-color: {driver.team_colour};
                color: #000000; /* Black text for better visibility */
                margin: 5px 0;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            .stat-card {{
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
            .results-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            .results-table th,
            .results-table td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            .results-table th {{
                background-color: #f8f9fa;
            }}
        </style>
    </head>
    <body>
        <div class="driver-card">
            <div class="driver-info">
                <img src="{driver.headshot_url}" alt="{driver.first_name} {driver.last_name}" class="driver-image">
                <div>
                    <h1>{driver.first_name} {driver.last_name}</h1>
                    <p><strong>Driver Number:</strong> #{driver.driver_number}</p>
                    <p><strong>Team:</strong> <span class="team-badge">{driver.team_name}</span></p>
                    <p><strong>Country:</strong> {driver.country_code}</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def open_in_browser(html_content: str) -> None:
    """Open HTML content in the default web browser."""
    try:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as temp:
            temp.write(html_content)
            temp.flush()
            webbrowser.open('file://' + temp.name)
    except Exception as e:
        print(f"Error opening browser: {str(e)}")
        print("You can view the driver information by copying the following HTML:")
        print(html_content)

def main():
    api = F1DriverAPI()
    
    while True:
        print("\nF1 Driver Information System")
        print("1. Search for a driver")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == '1':
            name = input("Enter driver name (e.g., 'Max' or 'Verstappen'): ").lower()
            print(f"\nSearching for drivers with name '{name}'...")
            
            drivers = api.search_drivers_by_name(name)
            
            if drivers:
                print(f"\nFound {len(drivers)} matching drivers:")
                for driver in drivers:
                    # Create HTML content for the driver
                    html = create_html(driver)
                    # Open in browser
                    open_in_browser(html)
            else:
                print("No drivers found with that name")
                
        elif choice == '2':
            print("\nGoodbye!")
            break
            
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()