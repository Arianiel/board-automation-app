import graph_ql_queries.graph_ql_functions as gql_queries


class IssueToUpdate:
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.project_to_use = None
        self.item_id = None

    def set_project(self, project):
        self.project_to_use = project

        set_proj_mutation = gql_queries.open_graph_ql_query_file("setProject.txt")

        result = gql_queries.run_query(
            set_proj_mutation.replace("[ISSUE_ID]", self.issue_id).replace("[PROJ_ID]", self.project_to_use.project_id))
        self.item_id = result["data"]["addProjectV2ItemById"]["item"]["id"]

    def set_sprint(self, sprint_to_use):
        setSprint = gql_queries.open_graph_ql_query_file("UpdateSprintForItemInProject.txt")
        print(gql_queries.run_query(setSprint.replace("[ITEM_ID]", self.item_id)
                                    .replace("[SPRINT_FIELD_ID]", self.project_to_use.sprint_field_id)
                                    .replace("[SPRINT_ID]", sprint_to_use)
                                    .replace("[PROJ_ID]", self.project_to_use.project_id)))

    def place_in_next_sprint(self):
        self.set_sprint(self.project_to_use.sprint_ids[self.project_to_use.next_sprint])