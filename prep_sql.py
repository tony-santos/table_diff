import re


def prep_sql(sql, original_source, new_source, original_target, new_target):
    # process source tables
    source_matches = re.finditer(rf"{original_source}.(\w+)", sql, re.IGNORECASE)
    sql_source_processed = sql
    for match in source_matches:
        old_dataset, table = match.group().split('.')
        print(f" dataset: {old_dataset}    table: {table}")
        sql_source_processed = re.sub(f"{original_source}.{table}", f"{{{{source('{new_source}', '{table}')}}}}", sql_source_processed)
    print(f"sql_source_processed: {sql_source_processed}")
    # process intermediate tables
    target_matches = re.finditer(rf"{original_target}.(\w+)", sql_source_processed, re.IGNORECASE)
    sql_target_processed = sql_source_processed
    for match in target_matches:
        old_target, table = match.group().split('.')
        print(f" dataset: {old_target}    table: {table}")
        sql_target_processed = re.sub(f"{original_target}.{table}", f"{{{{ref('{new_target}', '{table}')}}}}", sql_target_processed)
    print(f"sql_target_processed: {sql_target_processed}")
    return sql_target_processed


def prep_sql_sources(sql, original_source, new_source):
    # process source tables
    source_matches = re.finditer(rf"{original_source}.(\w+)", sql, re.IGNORECASE)
    sql_source_processed = sql
    for match in source_matches:
        old_dataset, table = match.group().split('.')
        print(f" dataset: {old_dataset}    table: {table}")
        sql_source_processed = re.sub(f"{original_source}.{table}", f"{{{{source('{new_source}', '{table}')}}}}", sql_source_processed)
    print(f"sql_source_processed: {sql_source_processed}")
    return sql_source_processed


def prep_sql_targets(sql, original_target, new_target):
    # process intermediate tables
    target_matches = re.finditer(rf"{original_target}.(\w+)", sql, re.IGNORECASE)
    sql_target_processed = sql
    for match in target_matches:
        old_target, table = match.group().split('.')
        print(f" dataset: {old_target}    table: {table}")
        sql_target_processed = re.sub(f"{original_target}.{table}", f"{{{{ref('{new_target}', '{table}')}}}}", sql_target_processed)
    print(f"sql_target_processed: {sql_target_processed}")


original_source = 'fake_source'
original_target = 'fake_target'
new_source = 'real_source'
new_target = 'real_target'
source_table1 = 'table1'
source_table2 = 'table2'
source_table3 = 'table3'
original_sql = f" from {original_source}.{source_table1} union all select * from {original_target}.{source_table2} union all select * from {original_source}.{source_table3}"
print(f"before: {original_sql}")

sql_with_source_dataset = prep_sql_sources(original_sql, original_source, new_source)
prepped_sql = prep_sql_targets(sql_with_source_dataset, original_target, new_target)
print(f"prepped_sql: {prepped_sql}")
exit(0)
matches = re.finditer(rf"{original_dataset}.(\w+)", s, re.IGNORECASE)
replaced2 = s
for match in matches:
    old_dataset, table = match.group().split('.')
    print(f" dataset: {old_dataset}    table: {table}")
    replaced2 = re.sub(f"{old_dataset}.{table}", f"{{{{source('{source_dataset}', '{table}')}}}}", replaced2)
print(f"replaced2: {replaced2}")
exit(0)
print(f" dataset: {old_dataset}    table: {table}")
replaced2 = re.sub(f"{old_dataset}.{table}", f"{{{{source('{source_dataset}', '{table}')}}}}", s)




