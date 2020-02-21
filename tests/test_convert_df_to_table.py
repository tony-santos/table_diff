# pytest --verbose -k test_convert_df_to_table

import pandas as pd
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import table_diff

@pytest.fixture
def df1by1():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01']

    return df

@pytest.fixture
def df2by1():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01', '2016-06-21']

    return df

@pytest.fixture
def df1by2():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01']
    df['float_column'] = [2200.0]

    return df

@pytest.fixture
def df2by2():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01', '2016-06-21']
    df['float_column'] = [2200.0, 2100.01]

    return df

@pytest.fixture
def df4():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df['float_column'] = [2200.0, 2100.01, 1500.00001000, 2100.123]
    df['integer_column'] = [2200, 2100, 1500, 22001]
    df['boolean_column'] = [True, False, False, True]

    return df

@pytest.fixture
def column_list():
    return ['date_column', 'float_column', 'integer_column', 'boolean_column']

def test_convert_df_to_table_date_one_row(df1by1):
    assert(['| date_column |\n', '| 2016-04-01  |\n'] == table_diff.convert_df_to_table(df1by1, ['date_column'], [11]))

def test_convert_df_to_table_date_two_rows(df2by1):
    assert(['| date_column |\n', '| 2016-04-01  |\n', '| 2016-06-21  |\n'] == table_diff.convert_df_to_table(df2by1, ['date_column'], [11]))

def test_convert_df_to_table_two_cols_one_row(df1by2):
    assert(['| date_column | float_column |\n', '| 2016-04-01  | 2200.0       |\n'] == table_diff.convert_df_to_table(df1by2, ['date_column', 'float_column'], [11, 12]))

def test_convert_df_to_table_two_cols_two_rows(df2by2):
    assert(['| date_column | float_column |\n', '| 2016-04-01  | 2200.0       |\n', '| 2016-06-21  | 2100.01      |\n'] == table_diff.convert_df_to_table(df2by2, ['date_column', 'float_column'], [11, 12]))

# def test_convert_df_to_table_integer(input_df):
#     assert(5 == table_diff.convert_df_to_table(input_df['integer_column']))

# def test_convert_df_to_table_float(input_df):
#     print(f"float_column: {input_df['float_column']}")
#     assert(10 == table_diff.convert_df_to_table(input_df['float_column']))

# def test_convert_df_to_table_boolean(input_df):
#     assert(5 == table_diff.convert_df_to_table(input_df['boolean_column']))
