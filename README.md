# F1 Driver Analyzer

#### Video Demo: https://www.youtube.com/watch?v=HKEPpvxaHUQ

#### Description:

The F1 Driver Analyzer is a Python application that provides comprehensive information about Formula 1 drivers. This tool allows users to search for drivers by name and view detailed information. The application is built with a focus on simplicity and user-friendliness, making it easy for F1 enthusiasts to get quick access to driver information.

## Project Structure

### Files

- `project.py`: The main application file containing the core functionality
  - Implements the `F1DriverAPI` class for making API requests to the OpenF1 API
  - Defines the `Driver` data class for storing driver information
  - Contains methods for fetching driver data
  - Handles HTML generation for displaying driver information

- `test_project.py`: Unit tests for the application
  - Tests the `search_drivers_by_name` functionality
  - Verifies error handling and edge cases
  - Ensures the application works as expected

- `requirements.txt`: Lists the required Python packages
  - `requests`: For making HTTP requests to the F1 API

### Key Features

   **Driver Search**
   - Search for drivers by first or last name (case-insensitive)
   - Displays driver information including:
     - Driver number
     - First and last name
     - Team name and color
     - Nationality
     - Headshot URL

## Design Decisions

### API Integration
- Chose to use the OpenF1 API for real-time data

### Data Structure
- Used Python's dataclasses for clean and maintainable data models
- Implemented proper type hints for better code clarity
- Created a modular API client class for easy extension

### User Interface
- Decided to use HTML for displaying results for better formatting
- Implemented a simple yet effective menu system
- Added proper error handling for file operations

## Usage

1. Run the application:
   ```bash
   python project.py
   ```

2. Use the menu to:
   - Search for drivers by name
   - Exit the program

3. View results in your default web browser

## Requirements

- Python 3.8+
- requests package (installed via requirements.txt)

## Testing

The project includes comprehensive unit tests that verify:
- Driver search functionality
- Error handling
- API response parsing
- Data structure integrity

To run tests:
```bash
pytest test_project.py