import get_project_info
import Test_Code.update_item_info as up_info

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

