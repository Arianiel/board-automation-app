from enum import Enum

## THIS IS NOT READY YET, CHANGING APPROACH

class Statuses(Enum):
    PROPOSAL = "proposal"
    IN_PROGRESS = "in progress"
    IMPEDED = "impeded"
    REVIEW = "review"
    REWORK = "rework"


# Reminders
# To get the value of an enum key
Statuses.REWORK.value
# To get an enum key from a value
Statuses("impeded").name
