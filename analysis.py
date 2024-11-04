"""
analysis.py

This module provides functions for analyzing and summarizing data within a pandas DataFrame. 
Currently, it includes the `group_and_count` function, which allows for efficient grouping 
and counting of data by specified columns, with optional merging capabilities for combining 
data from multiple DataFrames.

Functions:
- group_and_count: Groups the data by a specified column, counts occurrences of another column 
  if specified, and returns a summary DataFrame. This function also supports merging with another 
  DataFrame prior to grouping and counting, enabling more flexible data analysis workflows.

Dependencies:
- pandas
"""
import pandas as pd


def group_and_count(
    df: pd.DataFrame,
    groupby_column: str,
    count_column: str = None,
    merge_df: pd.DataFrame = None,
    merge_column_left: str = None,
    merge_column_right: str = None,
    count_column_name: str = 'COUNT'
) -> pd.DataFrame:
    """
    Generic grouping and counting function.

    This function groups the input DataFrame by the specified column and counts
    the occurrences of a specified count column. Optionally, it can merge
    with another DataFrame before performing the grouping and counting.

    Parameters:
    - df (pd.DataFrame): The DataFrame to group and count.
    - groupby_column (str): The column name to group by.
    - count_column (str, optional): The column name to count. If None, the function counts 
      the occurrences of the group.
    - merge_df (pd.DataFrame, optional): A DataFrame to merge with the input DataFrame.
    - merge_column_left (str, optional): The column name in the input DataFrame to merge on.
    - merge_column_right (str, optional): The column name in the merge DataFrame to merge on.
    - count_column_name (str, optional): The name of the resulting count column. Defaults 
      to 'COUNT'.

    Returns:
    - pd.DataFrame: A DataFrame with the grouped counts, indexed by the groupby_column.
    """

    # Merge if specified
    if merge_df is not None and merge_column_left and merge_column_right:
        df = pd.merge(df, merge_df, how='left',
                      left_on=merge_column_left, right_on=merge_column_right)

    # Perform grouping and counting
    if count_column:
        count_df = df.groupby(groupby_column)[
            count_column].count().reset_index(name=count_column_name)
    else:
        count_df = df.groupby(groupby_column).size(
        ).reset_index(name=count_column_name)

    return count_df.set_index(groupby_column)
