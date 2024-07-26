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
print(current_project.project_number)
print(current_project.project_id)
label_added = "proposal"
issue_id = "I_kwDOMZjARM6QZUHK"
project_id = "PVT_kwDOCn5jHs4AlGI7"

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


mutation1 = """mutation AddReactionToIssue {
    addReaction(input:{subjectId:"I_kwDOMZjARM6QZUHK",content:HOORAY}) {
        reaction {
            content
        }
        subject {
            id
        }
    }
  }"""

print(gql_queries.run_query(setProj))
print(gql_queries.run_query(mutation1))

match label_added:
    case "proposal":
        print("Proposed ticket being added to project")
    case _:
        print("Nothing to be done with this label: ", label_added)