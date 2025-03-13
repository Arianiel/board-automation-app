# Project Board Checks Interface

The rules defining the allowed states for the project boards
generate errors, that can be used to ensure that issues have
the meta information needed.

This information will be made available as a JSON string
that can then be either displayed, or as initially intended, be
accessed via Jenkins.

## Content of the JSON

### total_num
The total number of errors and warning found that do not
match the rules for the board checks

### error_num
The number of errors counted when undertaking board checks

### warning_num
The number of warnings counted when undertaking the board checks

### details
The list of errors and warnings.
