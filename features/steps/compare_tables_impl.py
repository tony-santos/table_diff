from behave import given, when, then
import pandas as pd
import numpy as np
import table_diff as td


def prepare_temp_table(context,table):
    tmp_table=bq_utils.handle_bq_naming(table)
    context.tmp_tables[table]=tmp_table
    return tmp_table

@given(u'an expected table')
def expected(context):
    # src_table = prepare_temp_table(context,'expected')
    df=pd.DataFrame(data=context.table, columns=context.table.headings)\
        .replace('', np.NaN)\
        .replace('NULL', np.NaN)\
        .replace('.', np.NaN)

    context.expected = df
    context.column_list = context.table.headings
    print(f"column_list: {context.column_list}")

@given(u'an actual table')
def actual(context):
    # src_table = prepare_temp_table(context,'actual')
    df=pd.DataFrame(data=context.table, columns=context.table.headings)\
        .replace('', np.NaN)\
        .replace('NULL', np.NaN)\
        .replace('.', np.NaN)

    context.actual = df

@when(u'the tables are compared')
def compared(context):
    context.tables_match = td.compare_dataframes_as_tables(context.expected, context.actual, context.column_list, context.column_list)

@then(u'tables match')
def compare_tables(context):
    assert context.tables_match == True

@then(u'tables do not match')
def compare_tables(context):
    assert context.tables_match == False

# @then(u'a {result} message is generated')
# def check_message(context, result):
#     pass