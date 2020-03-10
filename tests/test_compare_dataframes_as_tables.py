# pytest --verbose -vv -k test_compare_dataframes_as_tables

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
def df1by1a():

    df = pd.DataFrame()
    df['date_column'] = ['2016-04-02']

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

@pytest.fixture
def expected_output1by1_nomatch():
    output = '\nexpected:\n' + \
             '  | date_column |\n' +\
             '  | 2016-04-01  |\n' +\
             '\nactual:\n' +\
             '  | date_column |\n' +\
             '  | 2016-04-02  |\n' +\
             '\nexpected vs actual:\n' +\
             '  | date_column |\n' +\
             '- | 2016-04-01  |\n' +\
             '?            ^\n' +\
             '+ | 2016-04-02  |\n' +\
             '?            ^\n'
    return output

def test_compare_dataframes_as_tables_small_match(df1by1, expected_output1by1_match, capsys):
    # compare_dataframes_as_tables does not return anything and the results are sent stdout
    # use capsys feature to capture and access stdout
    matched = table_diff.compare_dataframes_as_tables(df1by1, df1by1, ['date_column'])
    captured = capsys.readouterr()
    # assert(expected_output1by1_match == captured.out)
    assert(matched == True)

def test_compare_dataframes_as_tables_small_nomatch(df1by1, df1by1a, expected_output1by1_nomatch, capsys):
    # compare_dataframes_as_tables does not return anything and the results are sent stdout
    # use capsys feature to capture and access stdout
    with capsys.disabled():
        print(expected_output1by1_nomatch)
        print("\n\n\n")
    matched = table_diff.compare_dataframes_as_tables(df1by1, df1by1a, ['date_column'])
    captured = capsys.readouterr()
    # assert(expected_output1by1_nomatch == captured.out)
    assert(matched == False)

def test_check_for_columns_match(df4):
    column_list = list(df4)
    assert table_diff.check_for_columns(df4, df4, column_list) == True

def test_check_for_columns_missing_actual(df4):
    column_list = list(df4)
    expected_df = df4
    actual_df = df4
    del actual_df[column_list[-1]]  # delete last column in column_list from actual_df
    assert table_diff.check_for_columns(expected_df, actual_df, column_list) == False

def test_check_for_columns_missing_actual(df4):
    column_list = list(df4)
    expected_df = df4.copy()
    actual_df = df4[column_list[:-1]] # exclude last column in column_list from actual_df
    assert table_diff.check_for_columns(expected_df, actual_df, column_list) == False

def test_check_for_columns_missing_expected(df4):
    column_list = list(df4)
    expected_df = df4[column_list[:-1]] # exclude last column in column_list from expected_df
    actual_df = df4
    assert table_diff.check_for_columns(expected_df, actual_df, column_list) == False

def test_check_for_columns_expected_different_name(df4):
    column_list = list(df4)
    expected_df = df4.copy()
    actual_df = df4.copy()
    expected_df.rename(columns={'boolean_column':'new_column_name'}, inplace=True)
    print(f"expected cols: {list(expected_df)}")
    assert table_diff.check_for_columns(expected_df, actual_df, column_list) == False

def test_check_for_columns_missing_from_both(df4):
    column_list = list(df4)
    expected_df = df4.copy()
    actual_df = df4.copy()
    column_list[-1] = 'new_column_name'
    assert table_diff.check_for_columns(expected_df, actual_df, column_list) == False

def test_compare_dataframes_as_tables_actual_empty(df4):
    expected_df = df4.copy()
    column_list = list(df4)
    actual_df = pd.DataFrame()
    assert table_diff.compare_dataframes_as_tables(expected_df, actual_df, column_list) == False

