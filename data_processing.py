"""
data_processing.py

This module provides a generic data preprocessing function that allows for flexible
transformation of a DataFrame, including cleaning, filtering, and adding calculated
fields based on custom criteria.

Functions:
- data_preprocess: Cleans and transforms data by performing tasks such as filtering
  rows, handling missing values, converting date columns, applying thresholds on 
  specified columns, and dynamically adding calculated columns.

Parameters for data_preprocess:
- df (pd.DataFrame): The input DataFrame to be preprocessed.
- dropna (bool): Indicates whether to drop rows with missing values.
- filter_column_values (dict): Filters rows based on specific column values.
- delay_threshold_column (str): Specifies the column to apply a maximum delay threshold.
- delay_threshold (float): The maximum delay value for filtering rows.
- datetime_column_info (dict): Contains instructions for converting specified columns
  to a datetime format.
- additional_columns (dict): Allows dynamic column creation by specifying columns to
  add with either static values or functions applied to existing columns.
- columns_to_drop (list): Names of columns to remove from the DataFrame.

Returns:
- pd.DataFrame: The cleaned and preprocessed DataFrame ready for further analysis.

This module is designed for use cases where data preprocessing involves multiple, customizable
steps to prepare data for analysis or modeling.
"""
from typing import Optional, Dict, Any
import pandas as pd


def data_preprocess(
    df: pd.DataFrame,
    dropna: bool = True,
    filter_column_values: Optional[Dict[str, list]] = None,
    delay_threshold_column: Optional[str] = None,
    delay_threshold: Optional[float] = None,
    datetime_column_info: Optional[Dict[str, Any]] = None,
    additional_columns: Optional[Dict[str, Any]] = None,
    columns_to_drop: Optional[list] = None,
) -> pd.DataFrame:
    """
    Generic data preprocessing function.

    This function applies various preprocessing steps to the input DataFrame,
    including dropping missing values, filtering rows based on column values,
    applying a delay threshold, converting columns to datetime format,
    adding additional computed columns, and dropping specified columns.

    Parameters:
    - df (pd.DataFrame): The DataFrame to preprocess.
    - dropna (bool, optional): Whether to drop rows with missing values. Defaults to True.
    - filter_column_values (dict, optional): A dictionary where keys are column names
      and values are lists of values to keep in those columns.
    - delay_threshold_column (str, optional): The column to apply the delay threshold to.
    - delay_threshold (float, optional): The maximum delay value to keep.
    - datetime_column_info (dict, optional): Information for converting columns to datetime.
      Should include 'columns' (list of date columns), 'time_column' (time column), and 'format'.
    - additional_columns (dict, optional): A dictionary of additional columns to add to the 
      DataFrame, where keys are column names and values are either callables or static values.
    - columns_to_drop (list, optional): A list of column names to drop from the DataFrame.

    Returns:
    - pd.DataFrame: The preprocessed DataFrame.
    """

    if dropna:
        df = df.dropna()

    # Apply column filters
    if filter_column_values:
        for col, values in filter_column_values.items():
            df = df[df[col].isin(values)]

    # Filter by delay threshold
    if delay_threshold_column and delay_threshold is not None:
        df = df[df[delay_threshold_column] <= delay_threshold]

    # Convert to datetime if specified
    if datetime_column_info:
        date_columns = datetime_column_info.get('columns', [])
        time_column = datetime_column_info.get('time_column')
        datetime_format = datetime_column_info.get('format', '%Y-%m-%d')
        df[time_column] = pd.to_datetime(
            df[date_columns[0]].astype(str) + '-' +
            df[date_columns[1]].astype(str) + '-' +
            df[date_columns[2]].astype(str) + ' ' +
            df[time_column].astype(str).str.zfill(4),
            format=datetime_format
        )

    # Add additional columns
    if additional_columns:
        for col, func_or_value in additional_columns.items():
            if callable(func_or_value):
                df[col] = func_or_value(df)
            else:
                df[col] = func_or_value

    # Drop columns if specified
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    return df
