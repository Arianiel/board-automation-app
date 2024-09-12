import graph_ql_interactions.graph_ql_functions as gql_queries
from collections import Counter
from datetime import datetime
from github_interactions.sprint_information import SprintInfo


class Burndown:
    def __init__(self, org_name, project_number, current_sprint_name, next_sprint_name):
        self.card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
        self.org_name = org_name
        self.project_number = project_number
        self.current_sprint_name = current_sprint_name
        self.next_sprint_name = next_sprint_name
        csv_headings="Date,Backlog,In Progress,Impeded,Review,Done"
        # TODO: If it doesn't exist create a burndown csv
        self.burndown_csv = "burndown-points.csv"

    def burndown_display(self):
        return "This will be a class for a burndown display"

    def update_csv(self):
        # TODO: Verify that the csv is correct for the sprint
        # TODO: Clear csv before appending on start of sprint
        result = gql_queries.run_query(self.card_info_query.replace("<ORG_NAME>", self.org_name).replace("<PROJ_NUM>", str(self.project_number)))
        card_statuses = []
        cards_to_refine = []
        # First split to a new iterable
        items = result["data"]["organization"]["projectV2"]["items"]["nodes"]
        # Get the cards in this sprint
        for item in items:
            # Split to a further iterable
            field_values = item["fieldValues"]["nodes"]
            for value in field_values:
                try:
                    if value["field"]["name"] == "Sprint" and value["name"] == self.current_sprint_name:
                        # Get rid of empty values
                        cards_to_refine.append([i for i in field_values if i])
                except KeyError:
                    # Section is empty ignore it
                    pass
        # Get the statuses for the cards in this sprint
        for card in cards_to_refine:
            for value in card:
                try:
                    if value["field"]["name"] == "Status":
                        card_statuses.append(value["name"])
                except KeyError:
                    # Nothing to worry about this doesn't exist
                    pass
        # Build the string for adding to the CSV file
        card_frequency = Counter(card_statuses)
        today = datetime.today().strftime("%Y-%m-%d")
        entry_list = [today, ",", str(card_frequency["Backlog"]), ",", str(card_frequency["In Progress"]), ",",
                      str(card_frequency["Impeded"]), ",", str(card_frequency["Review"]), ",",
                      str(card_frequency["Done"]), "\n"]
        entry = "".join(entry_list)
        # Append the entry to the CSV file
        with open(self.burndown_csv, "a") as f:
            f.write(entry)
