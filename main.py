"""
main.py

This script is the main entry point for analyzing flight delay data.
It loads data, preprocesses it, and performs analyses such as counting
delayed flights, summarizing the number of flights per airport, identifying
top airports and airlines by delay, and calculating average delay times.

Steps:
1. Load flight, airport, and airline data from specified CSV files.
2. Preprocess flight data with customizable cleaning and transformation steps.
3. Perform analyses:
   - Count the total number of delayed flights.
   - Calculate and display average delay time.
   - Count flights per airport and identify top airports by flight volume.
   - Count delayed flights per airline and identify top airlines by delay count.
   - Calculate and display average delay times per airport and identify top airports by delay.

Modules:
- data_processing: For data cleaning and preparation.
- analysis: For specific aggregation and counting operations.
- config: Contains configuration settings like file paths and filter parameters.

Execution:
Run this script directly to perform the analysis.
"""
import pandas as pd
from data_processing import data_preprocess
from analysis import group_and_count
import config


def main() -> None:
    """
    Main function to load flight data, preprocess it, analyze delays, and 
    summarize the results by airport and airline.

    This function performs the following tasks:
    1. Load flight, airport, and airline data from CSV files.
    2. Preprocess the flight data to clean and filter it.
    3. Calculate and print the number of delayed flights and average delay time.
    4. Count and display the number of flights per airport.
    5. Display the top 3 airports by the number of flights.
    6. Calculate and display the number of delayed flights per airline.
    7. Display the top 3 airlines by the number of delayed flights.
    8. Calculate and display the average delay per airport.
    9. Display the top 3 airports with the highest average delay.
    """

    # Load data
    flights_df: pd.DataFrame = pd.read_csv(
        config.FLIGHTS_CSV_PATH, low_memory=False)
    airports_df: pd.DataFrame = pd.read_csv(config.AIRPORTS_CSV_PATH)
    airlines_df: pd.DataFrame = pd.read_csv(config.AIRLINES_CSV_PATH)

    # Preprocess the flights data
    flights_df_cleaned: pd.DataFrame = data_preprocess(
        flights_df,
        dropna=True,
        filter_column_values={'ORIGIN_AIRPORT': config.FILTER_AIRPORTS},
        delay_threshold_column='DEPARTURE_DELAY',
        delay_threshold=config.DELAY_THRESHOLD,
        datetime_column_info={
            'columns': ['DAY', 'MONTH', 'YEAR'],
            'time_column': 'SCHEDULED_DEPARTURE',
            'format': '%d-%m-%Y %H%M'
        },
        additional_columns={'IS_DELAYED': lambda x: (
            x['DEPARTURE_DELAY'] >= 15).astype(int)},
        columns_to_drop=['YEAR', 'MONTH', 'DAY']
    )

    # Display initial overview of cleaned data
    print("Cleaned Flights Data Sample:")
    print(flights_df_cleaned.head())

    # Calculate and print the number of delayed flights
    delayed_flights: int = flights_df_cleaned['IS_DELAYED'].sum()
    print(
        f"\nNumber of Delayed Flights (>= {config.DELAY_THRESHOLD} mins): {delayed_flights}")

    # Calculate and display the average delay time
    avg_delay: float = flights_df_cleaned['DEPARTURE_DELAY'].mean()
    print(f"Average Departure Delay (minutes): {avg_delay:.2f}")

    # Count and display the number of flights per airport
    num_flights_df: pd.DataFrame = group_and_count(
        flights_df_cleaned,
        groupby_column='ORIGIN_AIRPORT',
        merge_df=airports_df,
        merge_column_left='ORIGIN_AIRPORT',
        merge_column_right='IATA_CODE',
        count_column_name='NUM_FLIGHTS'
    )
    print("\nNumber of Flights per Airport:")
    print(num_flights_df)

    # Display the top 3 airports by number of flights
    top_3_airports: pd.DataFrame = num_flights_df.nlargest(3, 'NUM_FLIGHTS')
    print("\nTop 3 Airports by Number of Flights:")
    print(top_3_airports)

    # Number of delayed flights per airline
    delayed_flights_per_airline: pd.DataFrame = flights_df_cleaned.groupby(
        'AIRLINE')['IS_DELAYED'].sum().reset_index()
    delayed_flights_per_airline = delayed_flights_per_airline.merge(
        airlines_df, left_on='AIRLINE', right_on='IATA_CODE')
    delayed_flights_per_airline.rename(
        columns={'IS_DELAYED': 'NUM_DELAYED_FLIGHTS'}, inplace=True)
    print("\nNumber of Delayed Flights per Airline:")
    print(delayed_flights_per_airline)

    # Display the top 3 airlines by number of delayed flights
    top_3_delayed_airlines: pd.DataFrame = delayed_flights_per_airline.nlargest(
        3, 'NUM_DELAYED_FLIGHTS')
    print("\nTop 3 Airlines by Number of Delayed Flights:")
    print(top_3_delayed_airlines)

    # Average delay per airport
    avg_delay_per_airport: pd.DataFrame = flights_df_cleaned.groupby(
        'ORIGIN_AIRPORT')['DEPARTURE_DELAY'].mean().reset_index()
    avg_delay_per_airport = avg_delay_per_airport.merge(
        airports_df, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
    avg_delay_per_airport.rename(
        columns={'DEPARTURE_DELAY': 'AVG_DELAY'}, inplace=True)
    print("\nAverage Departure Delay per Airport:")
    print(avg_delay_per_airport)

    # Display the top 3 airports with the highest average delay
    top_3_delayed_airports: pd.DataFrame = avg_delay_per_airport.nlargest(
        3, 'AVG_DELAY')
    print("\nTop 3 Airports by Average Departure Delay:")
    print(top_3_delayed_airports)


if __name__ == "__main__":
    main()
