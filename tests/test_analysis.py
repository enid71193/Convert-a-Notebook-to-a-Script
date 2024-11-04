"""
Unit tests for the `analysis` module.

This module contains tests for the `group_and_count` function, which performs
grouping and counting on a DataFrame.

Classes:
    TestAnalysis: Unit tests for `group_and_count` function.

Functions:
    test_group_and_count: Tests the grouping and counting functionality of 
    `group_and_count`.
"""

import unittest
import pandas as pd
from analysis import group_and_count


class TestAnalysis(unittest.TestCase):
    """
    Test case for functions in the analysis module.

    Attributes:
        sample_flights_df (pd.DataFrame): Sample data for testing flight delays by origin airport.
    """

    def setUp(self):
        """
        Sets up sample data for testing.

        This method initializes a DataFrame for sample flight data, containing
        origin airports and delay status.
        """
        self.sample_flights_df = pd.DataFrame({
            'ORIGIN_AIRPORT': ['JFK', 'LAX', 'JFK', 'ORD', 'LAX'],
            'IS_DELAYED': [1, 0, 1, 0, 1]
        })

    def test_group_and_count(self):
        """
        Tests the `group_and_count` function for correct grouping and counting results.

        This method verifies that the function correctly counts the number of flights
        per airport. It checks:
        - The correct count of flights per airport.
        """
        result_df = group_and_count(
            self.sample_flights_df,
            groupby_column='ORIGIN_AIRPORT',
            count_column_name='NUM_FLIGHTS'
        ).reset_index()  # Reset index to make 'ORIGIN_AIRPORT' a column

        # Expected counts for each airport
        expected_counts = {'JFK': 2, 'LAX': 2, 'ORD': 1}
        for airport, count in expected_counts.items():
            self.assertEqual(
                result_df[result_df['ORIGIN_AIRPORT'] == airport]['NUM_FLIGHTS'].values[0], count
            )

        # Verify columns are as expected
        self.assertListEqual(result_df.columns.tolist(), ['ORIGIN_AIRPORT', 'NUM_FLIGHTS'])


if __name__ == '__main__':
    unittest.main()
