import pandas as pd
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import table_diff

@pytest.fixture
def input_value():

    df1 = pd.DataFrame()
    df1['date_column'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df1['float_column'] = [2200.0, 2100.01, 1500.0000, 2100.123]
    df1['integer_column'] = [2200, 2100, 1500, 22001]
    df1['boolean_column'] = [True, False, False, True]

    return df1

def test_get_longest_entry_date(input_value):
    assert(table_diff.get_longest_entry(input_value['date_column']) == 10)

def test_get_longest_entry_integer(input_value):
    assert(table_diff.get_longest_entry(input_value['integer_column']) == 5)

def test_get_longest_entry_float(input_value):
    assert(table_diff.get_longest_entry(input_value['float_column']) == 9)

def test_get_longest_entry_boolean(input_value):
    assert(table_diff.get_longest_entry(input_value['boolean_column']) == 5)
