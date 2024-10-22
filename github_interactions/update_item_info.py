import graph_ql_interactions.graph_ql_functions as gql_queries


class IssueToUpdate:
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.project_to_use = None
        self.item_id = None
        self.repo_name = None

    def set_project(self, project):
        self.project_to_use = project
        set_proj_mutation = gql_queries.open_graph_ql_query_file("SetProject.txt")

        result = gql_queries.run_query(
            set_proj_mutation.replace("<ISSUE_ID>", self.issue_id).replace("<PROJ_ID>", self.project_to_use.project_id))
        self.item_id = result["data"]["addProjectV2ItemById"]["item"]["id"]

    def set_sprint(self, sprint_to_use):
        set_sprint = gql_queries.open_graph_ql_query_file("UpdateSprintForItemInProject.txt")
        gql_queries.run_query(set_sprint.replace("<ITEM_ID>", self.item_id)
                                    .replace("<SPRINT_FIELD_ID>", self.project_to_use.sprint_field_id)
                                    .replace("<SPRINT_ID>", sprint_to_use)
                                    .replace("<PROJ_ID>", self.project_to_use.project_id))

    def set_status(self, status_to_use):
        set_sprint = gql_queries.open_graph_ql_query_file("UpdateStatusForItemInProject.txt")
        gql_queries.run_query(set_sprint.replace("<ITEM_ID>", self.item_id)
                              .replace("<STATUS_FIELD_ID>", self.project_to_use.status_field_id)
                              .replace("<STATUS_ID>", status_to_use)
                              .replace("<PROJ_ID>", self.project_to_use.project_id))

    def place_in_next_sprint(self):
        self.set_sprint(self.project_to_use.sprint_ids[self.project_to_use.next_sprint])
        self.set_status(self.project_to_use.status_ids["Backlog"])

    def place_in_current_sprint(self):
        self.set_sprint(self.project_to_use.sprint_ids[self.project_to_use.current_sprint])

    def get_repo(self):
        get_repo_query = gql_queries.open_graph_ql_query_file("findIssueRepo.txt").replace("<ISSUE>", self.issue_id)
        self.repo_name = gql_queries.run_query(get_repo_query)["data"]["node"]["repository"]["name"]

    def add_label(self, label_id_to_add):
        update_labels = gql_queries.open_graph_ql_query_file("UpdateItemLabel.txt")
        gql_queries.run_query(update_labels.replace("<ISSUE>", self.issue_id).replace("<LABEL_ID>", label_id_to_add))

    def remove_label(self, label_id_to_remove):
        update_labels = gql_queries.open_graph_ql_query_file("RemoveLabel.txt")
        gql_queries.run_query(update_labels.replace("<ISSUE>", self.issue_id).replace("<LABEL_ID>", label_id_to_remove))
