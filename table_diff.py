import difflib
import sys
import pandas as pd
import pprint

def get_longest_entry(df_column):
    """return length of longest entry in a data frame column

    converts all entries in column to string format, applies len function on converted column, and returns the max length
    Arguments:
        df_column {dataframe_column (df['col_name'])} -- column of dataframe to be evaluated
    
    Returns:
        [int] -- integer containing length of longest entry (after conversion to string)
    """
    return max(df_column.astype(str).apply(len))

def get_column_widths(df1, df2, column_list):
    """calculate column widths for a text table to be used by difflib for comparison

    sets column width to the longest of the values in either dataframe or the label if label is longer than all entries
    Arguments:
        df1 {dataframe} -- dataframe 1
        df2 {dataframe} -- dataframe 2
        column_list {list} -- list of columns to be measured
    
    Returns:
        list -- list containing the length of each column in column_list argument
    """
    # for each column, take longest of entry in either dataframe or length of label
    column_widths = [max(get_longest_entry(df1[col]), get_longest_entry(df2[col]), len(col)) for col in column_list]

    return column_widths


def convert_df_to_table(df, column_list, column_widths, delimiter='|'):
    """convert dataframe into a delimited text table
    TODO: convert column_widths to a dictionary to eliminate accessing by index
    Arguments:
        df {[type]} -- [description]
        column_list {[list]} -- list containing names of the columns to be converted. since lists are ordered the columns in resulting table follow order of column_list 
        column_widths {[list]} -- list or dictionary containing the length of longest entry (or label if label longer than all entries) for this column 
        delimiter {[list]} -- character or string to be used to delimit/separate columns in table. default delimiter is '|'
    
    Returns:
        [list] -- table as a list. each table row is a separate string
    """

    # header row
    line = delimiter
    for ix, item in enumerate(column_list):
        line = line + f" {item.ljust(column_widths[ix])} {delimiter}"

    table = [f"{line}\n"]

    # data rows
    for _, row in enumerate(df[column_list].itertuples(index=False), 1):
        line = delimiter
        for ix, item in enumerate(list(row)):
            line = line + f" {str(item).ljust(column_widths[ix])} {delimiter}"

        table.append(f"{line}\n")

    return table

def print_table(table, label):
    print(f"\n{label}:")
    for row in table:
        print(f"  {row.rstrip()}")

def compare_tables(expected_df, actual_df, column_list, sort_by=None):
    """compares two tables and displays the results
    
    converts two pandas dataframes to text tables and then compares the tables as lists of strings using difflib
    Arguments:
        expected_df {[type]} -- dataframe containing the expected results
        actual_df {[type]} -- dataframe containing the actual results
        column_list {[type]} -- list of columns to be used to compare the two tables. all columns in column_list must be present in both tables
    
    Keyword Arguments:
        sort_by {[type]} -- list of columns to be used to sort tables before comparison. if no sort order is specified, all columns are used to sort the tables and column order is defined by column_list paramater
    """
    if sort_by is None:
        sort_by = column_list
    
    column_widths = get_column_widths(df1, df2, column_list)
    expected = convert_df_to_table(expected_df.sort_values(by=sort_by), column_list, column_widths, delimiter='|')
    actual = convert_df_to_table(actual_df.sort_values(by=sort_by), column_list, column_widths, delimiter='|')
    diff = difflib.ndiff(expected, actual)

    print_table(table=expected, label="expected")
    print_table(table=actual, label="actual")

    if expected == actual:
        print(f"\ntables match")
    else:
        print(f"\nexpected vs actual:")
        sys.stdout.writelines(diff)

if __name__ == "__main__":
    # column_list = ['date', 'calories', 'sleep hours', 'gym']
    column_list = ['gym', 'date', 'calories', 'sleep_hours']
    df1 = pd.DataFrame()
    df1['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df1['calories'] = [2200, 2100, 1500, 2100]
    df1['sleep_hours'] = [2200, 2100, 1500, 2200]
    df1['gym'] = [True, False, False, True]

    df2 = pd.DataFrame()
    df2['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02']
    df2['calories'] = [2200, 2200, 1500, 1500]
    df2['sleep_hours'] = [2200, 2100, 1600, 1500]
    df2['gym'] = [True, True, False, True]

    df3 = pd.DataFrame()
    df3['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03']
    df3['calories'] = [2200, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500]
    df3['sleep_hours'] = [2200, 2100, 1500, 2200, 2100, 2200, 2100, 2200, 2100, 2200, 2100, 2200, 2100]
    df3['gym'] = [True, False, False, True, False, True, False, True, False, True, False, True, False]

    df4 = pd.DataFrame()
    df4['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03']
    df4['calories'] = [2200, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500]
    df4['sleep_hours'] = [2200, 2100, 1500, 2200, 2100, 2200, 2100, 2200, 2100, 2200, 2100, 2200, 2100]
    df4['gym'] = [True, False, False, True, False, True, False, True, False, True, False, True, False]

    df5 = pd.DataFrame()
    df5['date'] = ['2016-04-01', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02', '2016-04-03', '2016-04-02']
    df5['calories'] = [2200, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100, 1500, 2100]
    df5['sleep_hours'] = [2200, 2100, 1500, 2200, 2100, 2200, 2100, 2200, 2100, 2200, 2100, 2200]
    df5['gym'] = [True, False, False, True, False, True, False, True, False, True, False, True]

    compare_tables(df1, df2, column_list, ['date'])
    compare_tables(df1, df1, column_list, ['sleep_hours', 'calories' ])

    compare_tables(df3, df4, column_list, ['date', 'gym'])
    compare_tables(df3, df5, column_list, ['date', 'gym'])
    compare_tables(df5, df3, column_list, ['date', 'gym'])
    # compare_tables(df1, df1, column_list, ['sleep_hours', 'calories' ])
