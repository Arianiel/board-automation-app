import graph_ql_interactions.graph_ql_functions as gql_queries
import graph_ql_interactions.card_interactions as cards
import graph_ql_interactions.repo_interactions as repos
import github_interactions.repo_information as repo_info
import github_interactions.project_increment_information as projects
import datetime
import configparser
import os
from burndown_interactions import burndown
import logging
import re

pm_logger = logging.getLogger('board_automation')


def build_html_table(info):
    data = "<table><tr>"
    for heading in info.keys():
        data += "<th>" + heading + "</th>"
    data += "</tr>"

    lengths = {}
    for item in info:
        lengths[item] = len(info[item])
    for i in range(max(lengths.values())):
        data += "<tr>"
        for item in info.keys():
            try:
                data += "<td>" + str(info[item][i]["number"]) + " (" + str(info[item][i]["repo"]) + ")</td>"
            except IndexError:
                data += "<td></td>"
        data += "</tr>"
    data += "</table>"
    return data


class AutomationInfo:
    def __init__(self):
        self.html_message = ""
        # Get values from config.ini
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))

        self.user_name = config["GITHUB.INTERACTION"]["user_name"]
        self.org_name = config["GITHUB.INTERACTION"]["org_name"]

        self.today = None
        self.today_day = None
        self.today_month = None
        self.today_year = None
        today = self.set_today()

        self.available_program_increments = {}
        self.current_project = None
        self.next_project = None
        self.update_projects(today)

        self.project_number = self.available_program_increments[self.current_project].number
        self.sprint_by_class = self.available_program_increments[self.current_project].sprint_by_class

        # Get current and next sprint
        self.current_sprint = ""
        self.next_sprint = ""
        self.set_current_and_next_sprint(today)
        self.current_burndown = burndown.Burndown(self.org_name, self.project_number, self.current_sprint,
                                                  self.next_sprint, self.sprint_by_class)

        # Initialise extra parameters needed
        self.repos = {}

    def add_repo(self, repo_name):
        if repo_name not in self.repos.keys():
            self.repos[repo_name] = repo_info.RepoInfo(self.org_name, repo_name)

    def set_today(self):
        # Get the date to use to automate some of the coding
        today = datetime.datetime.today()
        self.today_day = today.strftime("%d")
        self.today_month = today.strftime("%m")
        self.today_year = today.strftime("%Y")
        self.today = datetime.datetime(year=int(self.today_year), month=int(self.today_month), day=int(self.today_day))
        return today

    def set_current_and_next_sprint(self, today):
        self.current_sprint = None
        self.next_sprint = None
        for sprint in self.sprint_by_class.keys():
            if self.sprint_by_class[sprint] == today:
                self.current_sprint = sprint
            if self.sprint_by_class[sprint].sprint_start_date < today:
                try:
                    if self.sprint_by_class[self.current_sprint].sprint_start_date < \
                            self.sprint_by_class[sprint].sprint_start_date:
                        self.current_sprint = sprint
                except KeyError:
                    self.current_sprint = sprint
            if self.sprint_by_class[sprint].sprint_start_date > today:
                try:
                    if (self.sprint_by_class[self.next_sprint].sprint_start_date >
                            self.sprint_by_class[sprint].sprint_start_date):
                        self.next_sprint = sprint
                except KeyError:
                    self.next_sprint = sprint
        try:
            if self.sprint_by_class[self.next_sprint].in_next_pi:
                if not (self.available_program_increments[self.next_project].start_date > today):
                    self.html_message = "MAKE SURE THAT THE NEXT PI PROJECT IS CREATED!"
                    pm_logger.info("Next PI needed, and/or server restart needed")
        except KeyError:
            pm_logger.info("No sprints found")

    def update_sprints(self):
        self.update_projects(self.set_today())
        self.set_current_and_next_sprint(self.set_today())
        self.current_burndown.change_sprint()
        cards_to_refine = cards.get_card_issue_ids_in_sprint(org_name=self.org_name,
                                                             project_number=self.project_number,
                                                             sprint=self.current_sprint)
        for card in cards_to_refine:
            cards.remove_label(card, repos.get_label_id(org_name=self.org_name,
                                                        repo_name=cards.get_repo_for_issue(card),
                                                        label_name="proposal"))

    def update_projects(self, today):
        # Find the V2 projects owned by the organization
        self.html_message = ""
        proj_list_query = gql_queries.open_graph_ql_query_file("findProjects.txt")
        result_projects = \
            gql_queries.run_query(proj_list_query.replace("<ORG_NAME>", self.org_name))["data"]["organization"][
                "projectsV2"]["nodes"]

        # Filter out a dictionary of the PIs
        for result_project in result_projects:
            # Matching the title style and using the offset to help define if it is a PI or not
            try:
                is_pi = re.compile("PI_\d\d\d\d_\d\d").match(result_project["title"]).span()[0]
            except AttributeError:
                is_pi = -1
            if is_pi >= 0 and not result_project["template"] and not result_project["closed"]:
                if result_project["title"] not in self.available_program_increments.keys():
                    self.available_program_increments[result_project["title"]] = (projects.ProjectIncrement(
                        project_id=result_project["id"], number=result_project["number"], title=result_project["title"],
                        org_name=self.org_name))

        # Find the appropriate project for this PI
        # Set the values to the first entry in the dictionary as somewhere to start
        self.current_project = None
        self.next_project = None
        for program_increment in self.available_program_increments.keys():
            if self.available_program_increments[program_increment].PI_has_sprints:
                if self.current_project is None and self.next_project is None:
                    self.current_project = program_increment
                    self.next_project = program_increment
                else:
                    try:
                        if self.available_program_increments[program_increment].start_date < today:
                            if (self.available_program_increments[program_increment].start_date <
                                    self.available_program_increments[self.current_project].start_date):
                                self.current_project = program_increment
                        if self.available_program_increments[program_increment].start_date > today:
                            if (self.available_program_increments[program_increment].start_date <
                                    self.available_program_increments[self.next_project].start_date):
                                self.next_project = program_increment
                    except TypeError:
                        pm_logger.info("There is no start date for one of the PIs being looked at")
            else:
                pm_logger.info("There is a PI with no sprints set")

    def get_cards_snapshot(self):
        return cards.get_cards_and_points_snapshot_for_sprint(self.org_name, self.project_number, self.current_sprint)

    def get_sprint_columns_snapshot_html(self):
        info = cards.get_card_list_snapshot_for_sprint(self.org_name, self.project_number, self.current_sprint)
        data = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Issues in Columns</title></head>
        <body><h1>The present listings</h1>"""
        data += build_html_table(info)
        data += "</body></html>"
        return data

    def get_planning_priority_snapshot(self):
        info = cards.get_planning_snapshot(self.org_name, self.project_number, self.current_sprint)
        data = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Planning Priority</title></head>
        <body><h1>The present listings</h1>"""
        data += build_html_table(info)
        data += "</body></html>"
        return data

    def move_tickets_to_next_sprint(self):
        pass
