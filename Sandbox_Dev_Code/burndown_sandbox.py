import pandas.errors
import plotly.graph_objects as go
from datetime import datetime, timedelta
from github_interactions import automation_information
import numpy as np
import pandas as pd
import os
import graph_ql_interactions.graph_ql_functions as gql_queries
from collections import Counter
import logging

# current_project = get_project_info.ProjectInfo()
# print(current_project.current_sprint)
# print(current_project.next_sprint)
# # Simulate the inputs
# sprints = current_project.sprint_by_class
# current_sprint_name = current_project.current_sprint
# next_sprint_name = current_project.next_sprint
#
# # This is the code to start thinking about copying over
# start_date = sprints[current_sprint_name].sprint_start_date
# end_date = sprints[next_sprint_name].sprint_start_date
# # print(start_date)
# # print(end_date)
# # print((end_date-start_date).days)
#
# dates = start_date.isoformat()
# df = pd.read_csv("burndown-points.csv")
# start_index = 0
# dates = df["Date"][start_index:]
# last_line_index = len(dates)
#
# last_day = datetime.strptime(df["Date"][start_index + last_line_index - 1], "%Y-%m-%d")
#
# if datetime.today() > last_day:
#     print("This should see me adding a row")
#
#
# done = df["Done"].values[start_index:]
# backlog = df["Backlog"].values[start_index:]
# in_progres = df["In Progress"].values[start_index:]
# impeded = df["Impeded"].values[start_index:]
# review = df["Review"].values[start_index:]
#
# for i in range(1, (end_date-start_date).days + 1):
#     dates = np.append(dates, [(last_day + timedelta(days=i))])
#     if i > last_line_index:
#         done = np.append(done, [done[-1]])
#         backlog = np.append(backlog, [backlog[-1]])
#         in_progres = np.append(in_progres, [in_progres[-1]])
#         impeded = np.append(impeded, [impeded[-1]])
#         review = np.append(review, [review[-1]])

"""fig = go.Figure(
    go.Scatter(x=dates, y=done, name="Done", line_color="grey", mode="lines+markers"),
    layout_yaxis_title="Count",
)
fig.add_scatter(x=dates, y=backlog, name="Backlog", line_color="green", mode="lines+markers")
fig.add_scatter(x=dates, y=in_progres, name="In Progress", line_color="magenta", mode="lines+markers")
fig.add_scatter(x=dates, y=impeded, name="Impeded", line_color="red", mode="lines+markers")
fig.add_scatter(x=dates, y=review, name="Review", line_color="purple", mode="lines+markers")
"""
# fig = go.Figure(
#     data=[
#         go.Bar(
#             name="Done",
#             x=dates,
#             y=done,
#             text=done,
#             offsetgroup=0,
#         ),
#         go.Bar(
#             name="Review",
#             x=dates,
#             y=review,
#             text=review,
#             offsetgroup=0,
#             base=done,
#         ),
#         go.Bar(
#             name="Impeded",
#             x=dates,
#             y=impeded,
#             text=impeded,
#             offsetgroup=0,
#             base=review+done,
#         ),
#         go.Bar(
#             name="In Progress",
#             x=dates,
#             y=in_progres,
#             text=in_progres,
#             offsetgroup=0,
#             base=impeded+review+done,
#         ),
#         go.Bar(
#             name="Backlog",
#             x=dates,
#             y=backlog,
#             text=backlog,
#             offsetgroup=0,
#             base=in_progres+impeded+review+done,
#         ),
#     ],
#     layout=go.Layout(
#         title="Sprint Tracking",
#         legend=dict(
#             traceorder="reversed",
#         )
#     )
# )
#
# fig.update_layout(showlegend=True)
# fig.write_html("burndown-points.html")
# The setup section
current_project = get_project_info.AutomationInfo()
sprints = current_project.sprint_by_class
current_sprint_name = current_project.current_sprint
next_sprint_name = current_project.next_sprint
burndown_csv = os.path.join(os.path.dirname(__file__), "burndown-points.csv")
card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
org_name = current_project.org_name
project_number = current_project.project_number
csv_headings = "Date,Backlog,In Progress,Impeded,Review,Done\n"


# The other code needed
def get_new_csv_line():
    # Get the list of items in the project
    # Note that there should always be at least one page so the pagination is added afterwards
    result = gql_queries.run_query(card_info_query.
                                   replace("<ORG_NAME>", org_name).
                                   replace("<PROJ_NUM>", str(project_number)).
                                   replace("<AFTER>", "null"))
    has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
    items = []
    for item in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
        items.append(item)
    # Add items from any further pages
    while has_next_page:
        end_cursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
        result = gql_queries.run_query(card_info_query.
                                       replace("<ORG_NAME>", "ISISComputingGroup").
                                       replace("<PROJ_NUM>", str(project_number)).
                                       replace("<AFTER>", "\"" + end_cursor + "\""))
        has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
        for item in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
            items.append(item)

    # Get the cards in this sprint
    cards_to_refine = []
    for item in items:
        # Split to a further iterable
        field_values = item["fieldValues"]["nodes"]
        for value in field_values:
            try:
                if value["field"]["name"] == "Sprint" and value["name"] == current_sprint_name:
                    # Get rid of empty values
                    cards_to_refine.append([i for i in field_values if i])
            except KeyError:
                # Section is empty ignore it
                pass

    # Get the statuses for the cards in this sprint
    card_statuses = []
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
    today_inner = datetime.today().strftime("%Y-%m-%d")
    entry_list = [today_inner, ",", str(card_frequency["Backlog"]), ",", str(card_frequency["In Progress"]), ",",
                  str(card_frequency["Impeded"]), ",", str(card_frequency["Review"]), ",",
                  str(card_frequency["Done"]), "\n"]
    entry = "".join(entry_list)
    return entry


def add_csv_titles():
    with open(burndown_csv, "w") as f:
        f.write(csv_headings)


def add_csv_line():
    with open(burndown_csv, "a") as f:
        f.write(get_new_csv_line())


def get_data_frame():
    today = datetime.strptime(datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")

    # Make sure the file exists and has something in it (start for today)
    try:
        df_inner = pd.read_csv(burndown_csv)
    except (pandas.errors.EmptyDataError, FileNotFoundError):
        add_csv_titles()
        add_csv_line()
        return pd.read_csv(burndown_csv)

    # Get the last day listed in the file
    start_index_inner = 0
    dates_inner = df_inner["Date"][start_index_inner:]
    last_line_index_inner = len(dates_inner)
    try:
        last_day_inner = datetime.strptime(df_inner["Date"][start_index_inner + last_line_index_inner - 1], "%Y-%m-%d")
    except KeyError:
        # if there is no data just add for today
        add_csv_line()
        return pd.read_csv(burndown_csv)

    print(sprints[current_sprint_name])
    print(last_day_inner)
    print(sprints[next_sprint_name])
    if not (sprints[current_sprint_name].sprint_start_date < last_day_inner < sprints[next_sprint_name].sprint_start_date):
        pm_logger = logging.getLogger('board_automation')
        pm_logger.exception("The error from the burndown")
        print("This is my error state")

    if today > last_day_inner:
        if (today - last_day_inner).days > 1:
            fill_csv_lines(today, last_day_inner, df_inner.iloc[-1])
        add_csv_line()

    return pd.read_csv(burndown_csv)


def fill_csv_lines(today, last_day_inner, data):
    for missing_day in range((today - last_day_inner).days - 1):
        with open(burndown_csv, "a") as f:
            entry_list = [(last_day_inner + timedelta(days=(missing_day + 1))).strftime("%Y-%m-%d"), ",",
                          str(data["Backlog"]), ",", str(data["In Progress"]), ",",
                          str(data["Impeded"]), ",", str(data["Review"]), ",",
                          str(data["Done"]), "\n"]
            entry = "".join(entry_list)
            f.write(entry)


# The code I'm trying to resolve
# start_date = sprints[current_sprint_name].sprint_start_date
# end_date = sprints[next_sprint_name].sprint_start_date
#


df = get_data_frame()
# start_index = 0
# dates = df["Date"][start_index:]
# last_line_index = len(dates)
# last_day = datetime.strptime(df["Date"][start_index + last_line_index - 1], "%Y-%m-%d")
#
# done = df["Done"].values[start_index:]
# backlog = df["Backlog"].values[start_index:]
# in_progres = df["In Progress"].values[start_index:]
# impeded = df["Impeded"].values[start_index:]
# review = df["Review"].values[start_index:]
#
# for i in range(1, (end_date - start_date).days + 1):
#     dates = np.append(dates, [(last_day + timedelta(days=i))])
#     if i > last_line_index:
#         done = np.append(done, [done[-1]])
#         backlog = np.append(backlog, [backlog[-1]])
#         in_progres = np.append(in_progres, [in_progres[-1]])
#         impeded = np.append(impeded, [impeded[-1]])
#         review = np.append(review, [review[-1]])
# add_csv_titles()
