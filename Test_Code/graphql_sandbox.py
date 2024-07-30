import datetime
import graph_ql_queries.graph_ql_functions as gql_queries
import get_project_info

"""
current_project = get_project_info.ProjectInfo(True)
print(current_project.user_name)
print(current_project.orgs)
print(current_project.org_name)
print(current_project.result_projects)
print(current_project.project_id)
print(current_project.fields)
print(current_project.sprints)

print("--------------")

fields = current_project.fields
sprints = current_project.sprints

print("current_sprint: "+current_project.current_sprint)
print("next_sprint: "+current_project.next_sprint)
"""
current_project = get_project_info.ProjectInfo(True)
# print(current_project.fields)
# print(current_project.sprint_field_id)
# print(current_project.sprint_ids)
# print(current_project.sprint_ids[current_project.next_sprint])

label_added = "proposal"
issue_id = "I_kwDOMZjARM6QZUHK"
project_id = "PVT_kwDOCn5jHs4AlGI7"
sprint_field_id = "PVTSSF_lADOCn5jHs4AlGI7zgdNywk"
next_sprint_id = "b51ef428"

setProj = """ mutation setProject {
          addProjectV2ItemById(input: {
              contentId: "I_kwDOMZjARM6QZUHK",
              projectId: "PVT_kwDOCn5jHs4AlGI7"
          })
          {
              item{
                  id
              }
          }
      }"""

result = gql_queries.run_query(setProj)
print(result)
item_id = result["data"]["addProjectV2ItemById"]["item"]["id"]

# Item ID for this is the same one as is returned from set_proj
setSprint = """ mutation UpdateProject {
        updateProjectV2ItemFieldValue(input: { 
            projectId: "PVT_kwDOCn5jHs4AlGI7", 
            itemId: "[ITEM_ID]", 
            fieldId: "PVTSSF_lADOCn5jHs4AlGI7zgdNywk", 
            value: { 
                singleSelectOptionId: "b51ef428" 
                } 
        }) 
        {
            projectV2Item {
                id
            }
        }
    }

"""


print(gql_queries.run_query(setSprint.replace("[ITEM_ID]", item_id)))

"""
match label_added:
    case "proposal":
        print("Proposed ticket being added to project")
    case _:
        print("Nothing to be done with this label: ", label_added)
"""
