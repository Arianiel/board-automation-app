import get_project_info
import Test_Code.update_item_info as up_info
import graph_ql_queries.graph_ql_functions as ql

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

current_project = get_project_info.ProjectInfo(True)
print(current_project.status_ids)
print(current_project.status_ids["Backlog"])
label_added = "proposal"
issue_id = "I_kwDOMZjARM6QZUHK"
current_issue = up_info.IssueToUpdate(issue_id)
current_issue.set_project(current_project)

match label_added:
    case "proposal":
        print("Proposed ticket being added to project in next sprint")
        current_issue.place_in_next_sprint()
    case _:
        print("Nothing to be done with this label: ", label_added)
"""

#Add a label
check_repos = """
query ReposInProject {
  organization(login: "Arianiel"){
    login
    	projectV2(number: 1) {
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


check_repos = """
query findProjectSprints
{
    organization(login: "Arianiel"){
        projectV2(number: 1){
            ... on ProjectV2 {
                repositories(first: 5) {
                    nodes {
                        ... on Repository {
                            id
                        }
                    }
                }
                
                fields(first: 20) {
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


check_repos = """
query getIssueRepo {
  node(id: "I_kwDOMZjARM6U3OLH") {
    ... on Issue {
      number
      id
      repository {
        name
      }
    }
  }
}
"""

#print(ql.run_query(check_repos))

add_label = """
mutation UpdateItemLabels {
    addLabelsToLabelable(input: {
        labelableId: "I_kwDOMZjARM6U3OLH",
        labelIds: ["LA_kwDOMZjARM8AAAABr0GyUA"]
    })
    {
        clientMutationId
    }
}
"""

#print(ql.run_query(add_label))
"""
current_project = get_project_info.ProjectInfo(True)
print(current_project.repos)
current_project.add_repo("Test 1")
print(current_project.repos)
current_project.add_repo("Test 2")
print(current_project.repos)
current_project.add_repo("Test 3")
print(str(current_project.repos))

for entry in current_project.repos.keys():
    print(current_project.repos[entry])

testing = ["Test 2", "Test 4"]

for item in testing:
    if item not in current_project.repos.keys():
        print(item + " is not in there")
        current_project.add_repo(item)
    else:
        print(item + " is there")

for entry in current_project.repos.keys():
    print(current_project.repos[entry])
"""


# Check on a repo
query = """
query findRepoInfo {
  repository(owner: "Arianiel", name: "issues-repo") {
    name
    id
    labels(first: 100){
      nodes {
        name
        id
      }
    }
  }
}
"""

#print(ql.run_query(query))

current_project = get_project_info.ProjectInfo(True)
current_project.add_repo("issues-repo")

print(current_project.repos["issues-repo"].labels["bug"])
