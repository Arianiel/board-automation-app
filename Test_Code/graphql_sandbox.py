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

print(gql_queries.run_query(setProj))

setSprint = """ input {
    UpdateProjectV2ItemFieldValueInput: 
        fieldId: "PVTSSF_lADOCn5jHs4AlGI7zgdNywk"
        itemId: "I_kwDOMZjARM6QZUHK"
        projectId: "PVT_kwDOCn5jHs4AlGI7"
        value: "2024_08_01"
}
"""

test = """
{"query": mutation UpdateProject ($project: ID!, $item: ID!, $status_field: ID!, $status_value: String!) {
  updateProjectV2ItemFieldValue(input: { projectId: $project, itemId: $item, fieldId: $status_field, 
  value: { singleSelectOptionId: $status_value } }) {
    projectV2Item {
      id
    }
  }
},
"variables":
{
  "project": "PVT_kwDOCn5jHs4AlGI7", 
  "item": "I_kwDOMZjARM6QZUHK", 
  "status_field": "PVTSSF_lADOCn5jHs4AlGI7zgdNywk",
  "status_value": "2024_08_01"
}
}
"""


test = """
{
"query": "mutation ($myVar:AddReactionInput!) {
  addReaction(input:$myVar) {
    reaction {
      content
    }
    subject {
      id
    }
  }     
}",
"variables": {
  "myVar": {
    "subjectId":"I_kwDOMZjARM6QZUHK",
    "content":"HOORAY"
  }
}
}
"""
# Item ID for this is the same one as is returned from set_proj
test = """ mutation UpdateProject {
        updateProjectV2ItemFieldValue(input: { 
            projectId: "PVT_kwDOCn5jHs4AlGI7", 
            itemId: "PVTI_lADOCn5jHs4AlGI7zgRWjM8", 
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


print(gql_queries.run_query(test))

"""
match label_added:
    case "proposal":
        print("Proposed ticket being added to project")
    case _:
        print("Nothing to be done with this label: ", label_added)
"""
