# pytest --verbose -k test_compare_tables

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

@pytest.fixture
def expected_output1by1_match():
    return '\nexpected:\n  | date_column |\n  | 2016-04-01  |\n\nactual:\n  | date_column |\n  | 2016-04-01  |\n\ntables match\n'

# def test_compare_tables_small_match(df1by1, expected_output1by1, pytest.capsys):
#     captured = capsys.readouterr()
#     assert(expected_output1by1 == table_diff.compare_tables(df1by1, df1by1, ['date_column']))

def test_compare_tables_small_match(df1by1, expected_output1by1_match, capsys):
    # compare_tables does not return anything and the results are sent stdout
    # use capsys feature to capture and access stdout
    table_diff.compare_tables(df1by1, df1by1, ['date_column'])
    captured = capsys.readouterr()
    assert(expected_output1by1_match == captured.out)
