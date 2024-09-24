import plotly.graph_objects as go
from datetime import datetime, timedelta
from github_interactions import get_project_info
import numpy as np
import pandas as pd

current_project = get_project_info.ProjectInfo()
print(current_project.current_sprint)
print(current_project.next_sprint)
# Simulate the inputs
sprints = current_project.sprint_by_class
current_sprint_name = current_project.current_sprint
next_sprint_name = current_project.next_sprint

# This is the code to start thinking about copying over
start_date = sprints[current_sprint_name].sprint_start_date
end_date = sprints[next_sprint_name].sprint_start_date
# print(start_date)
# print(end_date)
# print((end_date-start_date).days)

dates = start_date.isoformat()
print("isofromat")
print(dates)
df = pd.read_csv("burndown-points.csv")
start_index = 0
dates = df["Date"][start_index:]
print("df")
print(dates)
last_line_index = len(dates)

last_day = datetime.strptime(df["Date"][start_index + last_line_index - 1], "%Y-%m-%d")

if datetime.today() > last_day:
    print("This should see me adding a row")


done = df["Done"].values[start_index:]
backlog = df["Backlog"].values[start_index:]
in_progres = df["In Progress"].values[start_index:]
impeded = df["Impeded"].values[start_index:]
review = df["Review"].values[start_index:]

for i in range(1, (end_date-start_date).days + 1):
    dates = np.append(dates, [(last_day + timedelta(days=i))])
    if i > last_line_index:
        done = np.append(done, [done[-1]])
        backlog = np.append(backlog, [backlog[-1]])
        in_progres = np.append(in_progres, [in_progres[-1]])
        impeded = np.append(impeded, [impeded[-1]])
        review = np.append(review, [review[-1]])

"""fig = go.Figure(
    go.Scatter(x=dates, y=done, name="Done", line_color="grey", mode="lines+markers"),
    layout_yaxis_title="Count",
)
fig.add_scatter(x=dates, y=backlog, name="Backlog", line_color="green", mode="lines+markers")
fig.add_scatter(x=dates, y=in_progres, name="In Progress", line_color="magenta", mode="lines+markers")
fig.add_scatter(x=dates, y=impeded, name="Impeded", line_color="red", mode="lines+markers")
fig.add_scatter(x=dates, y=review, name="Review", line_color="purple", mode="lines+markers")
"""
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
            base=review+done,
        ),
        go.Bar(
            name="In Progress",
            x=dates,
            y=in_progres,
            text=in_progres,
            offsetgroup=0,
            base=impeded+review+done,
        ),
        go.Bar(
            name="Backlog",
            x=dates,
            y=backlog,
            text=backlog,
            offsetgroup=0,
            base=in_progres+impeded+review+done,
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
fig.write_html("burndown-points.html")
