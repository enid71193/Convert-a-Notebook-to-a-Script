"""
Unit tests for the `data_processing` module.

This module contains tests for the `data_preprocess` function, which handles
data cleaning, filtering, and additional processing steps for flight data.

Classes:
    TestDataProcessing: Unit tests for `data_preprocess` function.

Functions:
    test_data_preprocess: Tests various data preprocessing steps including filtering,
                          column addition, and datetime handling.
"""

import unittest
import pandas as pd
from data_processing import data_preprocess


class TestDataProcessing(unittest.TestCase):
    """
    Test case for functions in the data_processing module.

    Attributes:
        sample_flights_df (pd.DataFrame): Sample data for testing preprocessing on flight delays.
    """

    def setUp(self):
        """
        Sets up sample data for testing.

        This method initializes a DataFrame containing sample flight data with columns for
        origin airports, departure delays, scheduled departure times, and date information.
        """
        self.sample_flights_df = pd.DataFrame({
            'ORIGIN_AIRPORT': ['JFK', 'LAX', 'JFK', 'ORD'],
            'DEPARTURE_DELAY': [20, -5, 30, 0],
            'SCHEDULED_DEPARTURE': ['1200', '1430', '0615', '0900'],
            'YEAR': [2020, 2020, 2020, 2020],
            'MONTH': [1, 1, 1, 1],
            'DAY': [1, 1, 1, 1]
        })

    def test_data_preprocess(self):
        """
        Tests the `data_preprocess` function for correct data filtering, column addition,
        and datetime handling.

        This method verifies:
        - The successful filtering of rows based on the specified origin airports.
        - The correct addition of the 'IS_DELAYED' column based on delay threshold.
        - The addition of a 'datetime' column and removal of the original date-related columns.
        """
        processed_df = data_preprocess(
            self.sample_flights_df,
            dropna=False,
            filter_column_values={'ORIGIN_AIRPORT': ['JFK', 'LAX']},
            delay_threshold_column='DEPARTURE_DELAY',
            delay_threshold=15,
            datetime_column_info={
                'columns': ['DAY', 'MONTH', 'YEAR'],
                'time_column': 'SCHEDULED_DEPARTURE',
                'format': '%d-%m-%Y %H%M'
            },
            additional_columns={'IS_DELAYED': lambda x: (x['DEPARTURE_DELAY'] >= 15).astype(int)},
            columns_to_drop=['YEAR', 'MONTH', 'DAY']
        )

        # Check if filtering retained only the rows with 'JFK' and 'LAX' in 'ORIGIN_AIRPORT'
        self.assertTrue(all(processed_df['ORIGIN_AIRPORT'].isin(['JFK', 'LAX'])))
        
        # Verify the presence of 'IS_DELAYED' and 'datetime' columns in the DataFrame
        self.assertIn('IS_DELAYED', processed_df.columns)
        self.assertIn('datetime', processed_df.columns)
        
        # Ensure date columns are removed
        self.assertNotIn('YEAR', processed_df.columns)
        self.assertNotIn('MONTH', processed_df.columns)
        self.assertNotIn('DAY', processed_df.columns)
        
        # Print processed DataFrame for debugging (optional)
        print(processed_df)

    if __name__ == '__main__':
        unittest.main()

