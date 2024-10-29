from github_interactions import get_project_info

project = get_project_info.ProjectInfo()
print("Project Created")
print(project.project_number)
print(project.sprint_ids)
print(project.current_sprint)
print(project.next_sprint)
print("Updating with a lied about date")
project.update_sprints()
print(project.current_sprint)
print(project.next_sprint)
