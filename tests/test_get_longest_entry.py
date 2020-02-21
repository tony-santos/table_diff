# pytest --verbose -k test_get_longest_entry

import pandas as pd
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import table_diff

@pytest.fixture
def input_df():

    df1 = pd.DataFrame()
    df1['date_column'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df1['float_column'] = [2200.0, 2100.01, 1500.00001000, 2100.123]
    df1['integer_column'] = [2200, 2100, 1500, 22001]
    df1['boolean_column'] = [True, False, False, True]

    return df1

@pytest.fixture
def column_list():
    return ['date_column', 'float_column', 'integer_column', 'boolean_column']

def test_get_longest_entry_date(input_df):
    assert(table_diff.get_longest_entry(10 == input_df['date_column']))

def test_get_longest_entry_integer(input_df):
    assert(table_diff.get_longest_entry(5 == input_df['integer_column']))

def test_get_longest_entry_float(input_df):
    print(f"float_column: {input_df['float_column']}")
    assert(table_diff.get_longest_entry(9 == input_df['float_column']))

def test_get_longest_entry_boolean(input_df):
    assert(table_diff.get_longest_entry(5 == input_df['boolean_column']))
