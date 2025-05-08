from unittest.mock import patch, Mock #for testing with mock data
from project import F1DriverAPI #imported from the project
import requests

def test_search_drivers_by_name():
    api = F1DriverAPI()
    
    # Mock response data
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            'driver_number': 1,
            'first_name': 'Lewis',
            'last_name': 'Hamilton',
            'team_name': 'Mercedes',
            'team_colour': '#00D2BE',
            'country_code': 'GBR',
            'headshot_url': 'https://example.com/hamilton.jpg'
        }
    ]
    
    with patch('requests.Session.get', return_value=mock_response):
        # Test with name search
        drivers = api.search_drivers_by_name('lewis')
        assert len(drivers) == 1
        assert drivers[0].first_name == 'Lewis'
        assert drivers[0].last_name == 'Hamilton'
        assert drivers[0].team_name == 'Mercedes'
        assert drivers[0].team_colour == '#00D2BE'

def test_search_drivers_by_name_no_results():
    api = F1DriverAPI()
    
    # Mock response with empty drivers list
    mock_response = Mock()
    mock_response.json.return_value = []
    
    with patch('requests.Session.get', return_value=mock_response):
        drivers = api.search_drivers_by_name('nonexistent')
        assert len(drivers) == 0

def test_search_drivers_by_name_error_handling():
    api = F1DriverAPI()
    
    # Mock response with error
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException('API Error')
    
    with patch('requests.Session.get', return_value=mock_response):
        drivers = api.search_drivers_by_name('lewis')
        assert len(drivers) == 0
        
        
        
        
#Let's test our project

#as you can see there are 3 tests PASSED

#and these 3 tests correspond to the code above

#test 1 out of 3 is searching a driver with results

#test 2 out of 3 is searching without results

#test 3 out of 3 is error handling All tests have been executed successfully, confirming the functionality of the driver search feature.

# All tests have passed, verifying that the F1DriverAPI search functionality works as expected.