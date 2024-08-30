from enum import Enum


class StatusLabels(Enum):
    PROPOSAL = "proposal"
    IN_PROGRESS = "in progress"
    IMPEDED = "impeded"
    REVIEW = "review"
    REWORK = "rework"


# Reminders
# To get the value of an enum key
StatusLabels.REWORK.value
# To get an enum key from a value
StatusLabels("impeded").name





"""
What do I want this to do?
I have a label name, this is a value that tells me what status it needs to have, this is a key
When a label is set there are varying actions to perform:
    put in the current project if not in it
    apply a sprint value for the current project if in it
    apply a status for the current project if in it
    apply a points value for the current project if in it
    
    
Label Added         Project             Sprint Value    Project Status  Project Points  
Proposal            Add if not in it    Next Sprint     Backlog         -
Added During Sprint Add if not in it    This Sprint     Backlog         -
In Progress         -                   -               In Progress     -
Impeded             -                   -               Impeded         -
Review              -                   -               Review          -
Rework              -                   -               Backlog         -
[points list]       -                   -               -               Set to matching value
bug
duplicate
fixed
for release
Friday
good first issue
needs pair review
no release notes
pair programme
re-requested
ready               -                   -               Backlog         -
sub ticket
support
training
umbrella
urgent
wontfix

Create a dictionary of points
Create a dictionary of labels which just set a project status
Create a dictionary of labels which add to project and sprint
Create a dictionary of labels that can be set by the status manager
Create a dictionary of any remaining labels
In each of the above, the key is the label, the value should be a dictionary of behaviours and the standard "colours"

e.g.
points_dict = {
    "0": {"value": 0, "appearance": ""},
    "1": {"value": 1, "appearance": ""}
}

or e.g.
add_to_proj = {
    "proposal": {"appearance": "", "sprint": "next"},
    "added during sprint": {"appearance": "", "sprint": "this"}
}

On linking to a project, get the list of labels for the current project, add any which don't exist
Make sure the colours are our "standard"

actually, a dictionary of labels with appearance then dictionaries for each of the above behavious might be better
"""