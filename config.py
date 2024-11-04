"""
config.py

This module defines configuration settings and constants used throughout the application. 
It includes file paths for input data files, as well as key parameters that control data 
filtering and thresholding in the analysis and preprocessing steps.

Constants:
- FLIGHTS_CSV_PATH (str): The file path to the flights data CSV file.
- AIRPORTS_CSV_PATH (str): The file path to the airports data CSV file.
- AIRLINES_CSV_PATH (str): The file path to the airlines data CSV file.
- FILTER_AIRPORTS (list): A list of airport codes to filter flights data by origin airport.
- DELAY_THRESHOLD (int): The delay threshold in minutes (defaulted to 24 hours) used to 
  classify flights as delayed.

These configuration settings are intended to centralize paths and parameters, allowing for 
easier adjustment and management of key settings in one place.
"""
# File paths
FLIGHTS_CSV_PATH = 'assets/flights.csv'
AIRPORTS_CSV_PATH = 'assets/airports.csv'
AIRLINES_CSV_PATH = 'assets/airlines.csv'

# Parameters
FILTER_AIRPORTS = ['BOS', 'JFK', 'SFO', 'LAX']
DELAY_THRESHOLD = 24 * 60  # In minutes, equivalent to 24 hours
