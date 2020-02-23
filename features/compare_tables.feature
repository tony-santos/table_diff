Feature: Compare tables

Scenario: Tables match
Given an expected table
| date_column | integer_column |
| 2019-02-02  | 1234567890     |
| 2019-02-03  | 23456789012345 |

And an actual table
| date_column | integer_column |
| 2019-02-02  | 1234567890     |
| 2019-02-03  | 23456789012345 |

When the tables are compared

Then compare_tables returns True

And a Tables match message is generated
