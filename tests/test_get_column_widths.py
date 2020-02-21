# pytest --verbose -k test_get_column_widths

import pandas as pd
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import table_diff

@pytest.fixture
def df1():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df['float_column'] = [2200.0, 2100.01, 1500.123456, 2100.123]
    df['integer_column'] = [2200, 2100, 1500, 123456789012345]
    df['boolean_column'] = [True, True, True, True]

    return df

@pytest.fixture
def df2():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df['float_column'] = [2200.0, 2100.01, 1500.123456789, 2100.123]
    df['integer_column'] = [2200, 2100, 1500, 22001]
    df['boolean_column'] = [True, False, False, True]

    return df

@pytest.fixture
def column_list():
    return ['date_column', 'float_column', 'integer_column', 'boolean_column']

# test when longest entry is in df1 and is longer than label
def test_get_column_widths_first(df1, df2):
    assert([15] == table_diff.get_column_widths(df1, df2, ['integer_column'] ))

# test when longest entry is in df2 and is longer than label
def test_get_column_widths_second(df1, df2):
    assert([14] == table_diff.get_column_widths(df1, df2, ['float_column'] ))

# test when longest entry is label
def test_get_column_widths_label(df1, df2):
    assert([14] == table_diff.get_column_widths(df1, df2, ['boolean_column'] ))

# test when longest entry is label
def test_get_column_widths_multiple_columns(df1, df2, column_list):
    assert([11, 14, 15, 14] == table_diff.get_column_widths(df1, df2, column_list ))
