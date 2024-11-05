import graph_ql_interactions.graph_ql_functions as gql_queries
import graph_ql_interactions.card_interactions as cards
import graph_ql_interactions.repo_interactions as repos
import github_interactions.repo_information as repo_info
import datetime
import configparser
import os
from burndown_interactions import burndown
from github_interactions.sprint_information import SprintInfo


class ProjectInfo:
    def __init__(self):
        # Get values from config.ini
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))

        self.user_name = config["GITHUB.INTERACTION"]["user_name"]
        self.org_name = config["GITHUB.INTERACTION"]["org_name"]

        # Get the users orgs
        orgs_query = gql_queries.open_graph_ql_query_file("findOrgs.txt")
        result = gql_queries.run_query(orgs_query.replace("<USER>", self.user_name))  # Execute the query
        self.orgs = result["data"]["user"]["organizations"]["nodes"]

        self.today = None
        self.today_day = None
        self.today_month = None
        self.today_year = None
        today = self.set_today()

        # Find the V2 projects owned by the organization
        self.proj_list_query = gql_queries.open_graph_ql_query_file("findProjects.txt")
        self.result_projects = \
            gql_queries.run_query(self.proj_list_query.replace("<ORG_NAME>", self.org_name))["data"]["organization"][
                "projectsV2"]["nodes"]
        projects = {}

        # Find the appropriate project for this PI
        self.project_number = "0"
        for result_project in self.result_projects:
            title = result_project["title"]
            self.project_id = result_project["id"]
            projects[title] = self.project_id
            if "PI" not in title:
                # At the moment I'm not interested in anything that isn't a PI
                pass
            if self.today_year in title:
                offset = title.find(self.today_year)
                pi_id = title[offset:offset + 7]
                pi_month = title[offset + 5:offset + 7]
                if int(pi_month) < int(self.today_month):
                    self.project_number = result_project["number"]
                    break
                elif int(pi_month) == int(self.today_month):
                    # This may be the first sprint of the PI, need to look into those dates
                    pass
                else:
                    # This is not the current PI, so I don't need to consider it in detail
                    pass

        if self.project_number == "0":
            return

        # Get custom fields
        self.sprint_list_id_query = gql_queries.open_graph_ql_query_file("findProjectSprints.txt")

        self.fields = gql_queries.run_query(
            self.sprint_list_id_query.replace("<PROJ_NUM>", str(self.project_number))
            .replace("<ORG_NAME>", self.org_name))["data"]["organization"]["projectV2"]["fields"]["nodes"]

        # Get sprint list
        self.sprints = {}
        self.sprint_ids = {}
        self.sprint_by_class = {}
        self.status_ids = {}
        for field in self.fields:
            match field["name"]:
                case "Sprint":
                    self.sprint_field_id = field["id"]
                    for option in field["options"]:
                        self.sprint_ids[option["name"]] = option["id"]
                        self.sprint_by_class[option["name"]] = SprintInfo(option)
                case "Status":
                    self.status_field_id = field["id"]
                    for option in field["options"]:
                        self.status_ids[option["name"]] = option["id"]
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

    def update_sprints(self):
        self.set_current_and_next_sprint(self.set_today())
        self.current_burndown.change_sprint()
        cards_to_refine = cards.get_card_ids_in_sprint(org_name=self.org_name,
                                                       project_number=self.project_number,
                                                       sprint=self.current_sprint)
        for card in cards_to_refine:
            cards.remove_label(card, repos.get_label_id(org_name=self.org_name,
                                                        repo_name=cards.get_repo_for_issue(card),
                                                        label_name="proposal"))
