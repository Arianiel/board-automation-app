# Ticket 34 - add reminder during last sprint of the PI to make sure that the next one exists

from github_interactions import automation_information
import graph_ql_interactions.card_interactions as cards
import graph_ql_interactions.graph_ql_functions as gql_queries

# current_project = automation_information.AutomationInfo()

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

# print(cards.get_cards_and_points_snapshot_for_sprint(org_name="ISISComputingGroup", project_number="20", sprint="2024_10_31"))

# set_sprint_mutation = gql_queries.open_graph_ql_query_file("UpdateSprintForItemInProject.txt")
#
# result = gql_queries.run_query(set_sprint_mutation.replace("<ITEM_ID>", "I_kwDOMZjARM6iNhwz")
#                           .replace("<SPRINT_FIELD_ID>", "PVTSSF_lADOCn5jHs4AsF7jzgjEqEM")
#                           .replace("<SPRINT_ID>", "2025_01_01")
#                           .replace("<PROJ_ID>", "6"))
#
# print(result)
#
# print(set_sprint_mutation.replace("<ITEM_ID>", "6")
#                           .replace("<SPRINT_FIELD_ID>", "PVTSSF_lADOCn5jHs4AsF7jzgjEqEM")
#                           .replace("<SPRINT_ID>", "2025_01_01")
#                           .replace("<PROJ_ID>", "6"))
# cards.get_cards_in_project("Arianiel", "6")

query = """
query findProjects {
  organization(login: "Arianiel"){
    login
      projectsV2(first: 100){
        nodes {
          id
          title
          number
          template
          closed
          }
        }
      }
    
"""

mutation = """
mutation UpdateSprintForItemInProject {
    updateProjectV2ItemFieldValue(input: {
        projectId: "PVT_kwDOCn5jHs4AsF7j",
        itemId: "PVTI_lADOCn5jHs4AsF7jzgVb-9E",
        fieldId: "PVTSSF_lADOCn5jHs4AsF7jzgjEqEM",
        value: {
            singleSelectOptionId: "cc350787"
        }
    })
    {
        projectV2Item {
            id
        }
    }
}
"""

mutation1 = """
mutation UpdateIssue {
    updateIssue(input: {
        id: "I_kwDOMZjARM6iNhwz"
        
    }
}
"""

query = """
query ReposInProject {
  organization(login: "Arianiel"){
    login
    	projectV2(number: 6) {
      	title
      	id
      	repositories (first: 5) {
          nodes {
            ... on Repository {
                name
                id
                labels (first: 5) {
                    nodes {
                        name
                        id
                    }
                }
            }
          }
        }
    }
  }
}
"""

query = """
query findProjectSprints
{
    organization(login: "Arianiel"){
        projectV2(number: 6){
            ... on ProjectV2 {
                fields(first: 100) {
                    nodes {
                        ... on ProjectV2Field {
                            name
                            id
                        }
                        ... on ProjectV2SingleSelectField {
                            name
                            id
                            options {
                                name
                                id
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

print(gql_queries.run_query(query))
print(gql_queries.run_query(mutation))

print(cards.get_cards_in_project("Arianiel", "6"))
