
# Flight Data Analysis

## Introduction

This project analyzes flight data to uncover insights about delays, the performance of different airlines, and airport efficiency. It processes raw flight and airport data, applies various preprocessing steps, and performs analyses such as counting flights, calculating average delays, and identifying the top airlines and airports based on performance metrics. The output includes summaries and statistics that help in understanding flight operations. The origin for this project was assignment 4 from siads 505. 

## Setup Instructions

To run the script, you need to set up your environment with the required packages and data files.

### Required Packages
- pandas
- numpy


## Execution
The main script, main.py, executes the following steps:

Data Loading: Reads the flight, airport, and airline data from CSV files using Pandas.

Data Preprocessing: Cleans the flight data by dropping missing values, filtering based on specified criteria, and converting date and time columns to a unified datetime format.

Flight Analysis:

Calculates the number of delayed flights and the average delay time.
Counts the number of flights per airport and identifies the top three airports by flight volume.
Computes the number of delayed flights per airline and identifies the top three airlines with the highest number of delayed flights.
Calculates the average departure delay per airport and identifies the airports with the highest average delays.
Output: Displays the results of the analyses, including summaries of cleaned data, counts of delayed flights, and the top-performing airlines and airports.

To run the analysis, execute the following command in your terminal:

python main.py