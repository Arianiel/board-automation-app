# Ticket 34 - add reminder during last sprint of the PI to make sure that the next one exists
from github_interactions import automation_information
import graph_ql_interactions.card_interactions as cards

current_project = automation_information.AutomationInfo()
# print(current_project.current_sprint)
# print(current_project.next_sprint)
# print("ids")
# for thing in current_project.sprint_ids:
#     print(thing)
# print("class")
# for thing in current_project.sprint_by_class:
#     print(thing)
# print(current_project.sprint_by_class[current_project.current_sprint].in_next_pi)
# print(current_project.sprint_by_class[current_project.next_sprint].in_next_pi)

# import github_interactions.project_increment_information as projects
#
# test = projects.ProjectIncrement(project_id=1, number=2, title="What")
# print(test)

# print(cards.get_number_of_cards_by_status(org_name="Arianiel", project_number="1", sprint="2024_11_01"))

# print(cards.get_cards_and_points_snapshot_for_sprint(org_name="Arianiel", project_number="1", sprint="2024_11_01"))
