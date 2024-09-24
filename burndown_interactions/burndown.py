import graph_ql_interactions.graph_ql_functions as gql_queries
from collections import Counter
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import os

class Burndown:
    def __init__(self, org_name, project_number, current_sprint_name, next_sprint_name, sprints):
        self.card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
        self.org_name = org_name
        self.project_number = project_number
        self.current_sprint_name = current_sprint_name
        self.next_sprint_name = next_sprint_name
        self.sprints = sprints
        self.csv_headings = "Date,Backlog,In Progress,Impeded,Review,Done"
        # TODO: If it doesn't exist create a burndown csv
        self.burndown_web_page = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates", "burndown-points.html"))
        self.burndown_csv = os.path.join(os.path.dirname(__file__), "burndown-points.csv")
        self.last_update = None
        self.update_display()

    def burndown_display(self):
        return "This will be a class for a burndown display"

    def update_display(self):
        start_date = self.sprints[self.current_sprint_name].sprint_start_date
        end_date = self.sprints[self.next_sprint_name].sprint_start_date

        df = pd.read_csv(self.burndown_csv)
        start_index = 0
        dates = df["Date"][start_index:]
        last_line_index = len(dates)

        last_day = datetime.strptime(df["Date"][start_index + last_line_index - 1], "%Y-%m-%d")
        today = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        if today > last_day:
            self.update_csv()
        self.last_update = today

        done = df["Done"].values[start_index:]
        backlog = df["Backlog"].values[start_index:]
        in_progres = df["In Progress"].values[start_index:]
        impeded = df["Impeded"].values[start_index:]
        review = df["Review"].values[start_index:]

        for i in range(1, (end_date - start_date).days + 1):
            dates = np.append(dates, [(last_day + timedelta(days=i))])
            if i > last_line_index:
                done = np.append(done, [done[-1]])
                backlog = np.append(backlog, [backlog[-1]])
                in_progres = np.append(in_progres, [in_progres[-1]])
                impeded = np.append(impeded, [impeded[-1]])
                review = np.append(review, [review[-1]])

        fig = go.Figure(
            data=[
                go.Bar(
                    name="Done",
                    x=dates,
                    y=done,
                    text=done,
                    offsetgroup=0,
                ),
                go.Bar(
                    name="Review",
                    x=dates,
                    y=review,
                    text=review,
                    offsetgroup=0,
                    base=done,
                ),
                go.Bar(
                    name="Impeded",
                    x=dates,
                    y=impeded,
                    text=impeded,
                    offsetgroup=0,
                    base=review + done,
                ),
                go.Bar(
                    name="In Progress",
                    x=dates,
                    y=in_progres,
                    text=in_progres,
                    offsetgroup=0,
                    base=impeded + review + done,
                ),
                go.Bar(
                    name="Backlog",
                    x=dates,
                    y=backlog,
                    text=backlog,
                    offsetgroup=0,
                    base=in_progres + impeded + review + done,
                ),
            ],
            layout=go.Layout(
                title="Sprint Tracking",
                legend=dict(
                    traceorder="reversed",
                )
            )
        )

        fig.update_layout(showlegend=True)
        fig.write_html(self.burndown_web_page)

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
