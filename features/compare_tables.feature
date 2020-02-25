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

Then tables match

Scenario: Tables do not match
Given an expected table
| date_column | integer_column |
| 2019-02-02  | 1234567890     |
| 2019-02-03  | 23456789012345 |

And an actual table
| date_column | integer_column |
| 2019-02-02  | 12345678901     |
| 2019-02-03  | 23456789012345 |

When the tables are compared

Then tables do not match

Scenario: Table has null column
Given an expected table
| STUDYID        | USUBJID                | IDVARVAL | QORIG   | QEVAL |
| ABC 123456-001 | ABC 123456-001-1010001 | 1        | DERIVED |       |
| ABC 123456-001 | ABC 123456-001-1010001 | 2        | DERIVED |       |
| ABC 123456-001 | ABC 123456-001-1010001 | 3        | DERIVED |       |

And an actual table
| STUDYID        | USUBJID                | IDVARVAL | QORIG   | QEVAL |
| ABC 123456-001 | ABC 123456-001-1010001 | 1        | DERIVED |       |
| ABC 123456-001 | ABC 123456-001-1010001 | 2        | DERIVED |       |
| ABC 123456-001 | ABC 123456-001-1010001 | 3        | DERIVED |       |

When the tables are compared

Then tables match

