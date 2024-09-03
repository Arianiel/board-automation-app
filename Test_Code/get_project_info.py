import graph_ql_queries.graph_ql_functions as gql_queries
import repo_information as repo_info
import datetime


class ProjectInfo:
    def __init__(self, test_status):
        # TODO make this something more variable than me
        self.user_name = "KathrynBaker"

        # Get the users orgs
        orgs_query = gql_queries.open_graph_ql_query_file("findOrgs.txt")
        result = gql_queries.run_query(orgs_query.replace("<USER>", self.user_name))  # Execute the query
        self.orgs = result["data"]["user"]["organizations"]["nodes"]

        # Assign the organization to use
        # TODO make this a parameter rather than magic values
        if test_status is True:
            self.org_name = "Arianiel"
        else:
            self.org_name = "ISISComputingGroup"

        # TODO verify that the organisation in use is in the available orgs for the user for the token

        # Get the date to use to automate some of the coding
        today = datetime.datetime.today()
        today_day = today.strftime("%d")
        today_month = today.strftime("%m")
        today_year = today.strftime("%Y")
        self.today = datetime.datetime(year=int(today_year), month=int(today_month), day=int(today_day))

        # Find the V2 projects owned by the organization
        self.proj_list_query = gql_queries.open_graph_ql_query_file("findProjects.txt")
        self.result_projects = gql_queries.run_query(self.proj_list_query.replace("<ORG_NAME>", self.org_name))["data"]["organization"]["projectsV2"]["nodes"]
        projects = {}

        # Find the appropriate project for this PI
        self.project_number = "0"
        for result_project in self.result_projects:
            title = result_project["title"]
            self.project_id = result_project["id"]
            projects[title] = self.project_id
            if "PI" in title:
                print("It would be a PI")
            if today_year in title:
                offset = title.find(today_year)
                pi_id = title[offset:offset + 7]
                print(pi_id)
                pi_month = title[offset + 5:offset + 7]
                if int(pi_month) < int(today_month):
                    self.project_number = result_project["number"]
                elif int(pi_month) == int(today_month):
                    # Need to look into the sprints and the date here
                    pass
                else:
                    print("This is not the PI I'm looking for")

        if test_status is True:
            self.project_number = "1"

        if self.project_number == "0":
            return

        # Get custom fields
        self.sprint_list_id_query = gql_queries.open_graph_ql_query_file("findProjectSprints.txt")

        self.fields = gql_queries.run_query(
            self.sprint_list_id_query.replace("<PROJ_NUM>", self.project_number).replace("<ORG_NAME>", self.org_name))[
            "data"]["organization"]["projectV2"]["fields"]["nodes"]

        # Get sprint list
        self.sprints = {}
        self.sprint_ids = {}
        self.status_ids = {}
        for field in self.fields:
            match field["name"]:
                case "Sprint":
                    self.sprint_field_id = field["id"]
                    for option in field["options"]:
                        if "Next" in option["name"]:
                            sprint_name = option["name"][9:-1]
                        else:
                            sprint_name = option["name"]
                        sprint_year = sprint_name[:4]
                        sprint_month = sprint_name[5:7]
                        sprint_day = sprint_name[8:]
                        self.sprints[option["name"]] = datetime.datetime(year=int(sprint_year), month=int(sprint_month),
                                                                    day=int(sprint_day))
                        self.sprint_ids[option["name"]] = option["id"]
                case "Status":
                    self.status_field_id = field["id"]
                    for option in field["options"]:
                        self.status_ids[option["name"]] = option["id"]
        # Get current and next sprint
        self.current_sprint = ""
        self.next_sprint = ""
        for sprint in self.sprints:
            if self.sprints[sprint] == self.today:
                self.current_sprint = sprint
            if self.sprints[sprint] < self.today:
                try:
                    if self.sprints[self.current_sprint] < self.sprints[sprint]:
                        self.current_sprint = str(sprint)
                except KeyError:
                    self.current_sprint = sprint
            if self.sprints[sprint] > self.today:
                try:
                    if self.sprints[self.next_sprint] > self.sprints[sprint]:
                        self.next_sprint = str(sprint)
                except KeyError:
                    self.next_sprint = sprint

        # Initialise extra parameters needed
        self.repos = {}

    def add_repo(self, repo_name):
        if repo_name not in self.repos.keys():
            self.repos[repo_name] = repo_info.RepoInfo(self.org_name, repo_name)