import datetime
from unittest import TestCase
from unittest.mock import patch, PropertyMock

import requests_mock

from Tests.test_helpers import issue_entry, pull_request_entry, draft_issue_entry, build_response, \
    QlCommand, PiDefaultResponseValues
from github_interactions.automation_information import AutomationInfo
from github_interactions.card_info import CardInfo
from github_interactions.project_increment_information import ProjectIncrement
from github_interactions.repo_information import RepoInfo
from github_interactions.sprint_information import SprintInfo

url = 'https://api.github.com/graphql'

class TestAutomationInfo(TestCase):

    @patch('github_interactions.automation_information.AutomationInfo.set_previous_current_and_next_sprint')
    @patch('github_interactions.automation_information.AutomationInfo.update_projects')
    def test_automation_info_dummy(self, mock_update_projects, mock_set_prev_next):
        # Please note, there will be red text displayed in relation to the missing Burndown information in this test,
        # but the test should pass
        try_class = AutomationInfo()
        mock_update_projects.assert_called()
        mock_set_prev_next.assert_called()
        self.assertEqual(try_class.today_year, datetime.datetime.today().strftime("%Y"))

    @requests_mock.mock()
    @patch('github_interactions.automation_information.AutomationInfo.set_previous_current_and_next_sprint')
    @patch('github_interactions.automation_information.AutomationInfo.update_projects')
    def test_add_repo(self, m, mock_update_projects, mock_set_prev_next):
        # Set up the class instance, and check that repos are empty
        try_class = AutomationInfo()
        mock_update_projects.assert_called()
        mock_set_prev_next.assert_called()
        self.assertEqual(try_class.repos, {})

        # Add the first repo
        test_repos = {}
        repo_1 = "Repo 1"
        test_repos[repo_1] = repo_1
        m.post(url, text=build_response(QlCommand.findRepoInfo, repo_name=repo_1, expected_labels={}),
               status_code=200)
        try_class.add_repo(repo_1)
        self.assertEqual(try_class.repos.keys(), test_repos.keys())

        # Add a second repo
        repo_2 = "Repo 2"
        test_repos[repo_2] = repo_2
        m.post(url, text=build_response(QlCommand.findRepoInfo, repo_name=repo_2, expected_labels={}),
               status_code=200)
        try_class.add_repo(repo_2)
        self.assertEqual(try_class.repos.keys(), test_repos.keys())

        # Re-add the first repo
        m.post(url, text=build_response(QlCommand.findRepoInfo, repo_name=repo_1, expected_labels={}),
               status_code=200)
        try_class.add_repo(repo_1)
        self.assertEqual(try_class.repos.keys(), test_repos.keys())

    @patch('github_interactions.automation_information.AutomationInfo.set_previous_current_and_next_sprint')
    @patch('github_interactions.automation_information.AutomationInfo.update_projects')
    def test_set_today(self, mock_update_projects, mock_set_prev_next):
        try_class = AutomationInfo()
        mock_update_projects.assert_called()
        mock_set_prev_next.assert_called()
        self.assertEqual(try_class.today_year, datetime.datetime.today().strftime("%Y"))
        self.assertEqual(try_class.today_month, datetime.datetime.today().strftime("%m"))
        self.assertEqual(try_class.today_day, datetime.datetime.today().strftime("%d"))
        self.assertEqual(try_class.today, datetime.datetime(year=int(try_class.today_year), month=int(try_class.today_month), day=int(try_class.today_day)))

    @patch('github_interactions.automation_information.AutomationInfo.update_projects')
    def test_set_previous_current_and_next_sprint(self, mock_update_projects):
        # Creating an instance of the object with the method under test patched locally
        with patch('github_interactions.automation_information.AutomationInfo.set_previous_current_and_next_sprint'):
            try_class = AutomationInfo()
        mock_update_projects.assert_called()

        # Test the method with attributes patched
        sprint_id = "sprint_id"
        today_to_use = datetime.datetime(year=2025, month=2, day=20)
        previous_sprint = datetime.datetime(year=2025, month=1, day=1)
        current_sprint = datetime.datetime(year=2025, month=2, day=2)
        next_sprint = datetime.datetime(year=2025, month=3, day=3)
        sprint_start_dates = [previous_sprint, current_sprint, next_sprint]
        sprint_start_dates.sort()
        sprint_by_class = {}
        for start_date in sprint_start_dates:
            sprint_by_class[start_date.strftime("%Y_%m_%d")] = SprintInfo({"name": start_date.strftime("%Y_%m_%d"), "id": sprint_id})
        
        with (patch.object(try_class, 'sprint_starts', sprint_start_dates), patch.object(try_class, 'today', today_to_use), 
              patch.object(try_class, 'sprint_by_class', sprint_by_class)):
            try_class.set_previous_current_and_next_sprint()
            self.assertEqual(try_class.current_sprint, current_sprint.strftime("%Y_%m_%d"))
            self.assertEqual(try_class.next_sprint, next_sprint.strftime("%Y_%m_%d"))
            self.assertEqual(try_class.previous_sprint, previous_sprint.strftime("%Y_%m_%d"))
    
    def test_update_sprints(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_update_projects(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_cards_snapshot(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_sprint_columns_snapshot_html(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_planning_priority_snapshot(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_move_tickets_to_next_sprint(self):
        # TODO
        # Figure out how to test this!
        pass
    
class TestCardInfo(TestCase):
    # Test 1: Empty dict -> error
    def test_empty_card(self):
        self.assertRaises(KeyError, CardInfo, {})

    # Test 2: Issue with everything
    def test_issue_with_all(self):
        card_ident = 2
        repo_name = "Repo"
        expected_labels = {"label_1": "label_1_id", "label_2": "label_2_id", "label_3": "label_3_id"}
        sprint = "Sprint"
        status = "Status"
        points = 10
        priority = "Medium"
        provided_fields = {"Points": points, "Planning Priority": priority, "Status": status, "Sprint": sprint}
        class_response = CardInfo(issue_entry(ident=card_ident, labels=expected_labels, fields=provided_fields, repo_name=repo_name))
        self.assertEqual(class_response.node_id, f"node_{card_ident}")
        self.assertEqual(class_response.type, "ISSUE")
        self.assertEqual(class_response.id, f"issue_{card_ident}")
        self.assertEqual(class_response.number, card_ident)
        self.assertEqual(class_response.repo, repo_name)
        self.assertEqual(class_response.labels, list(expected_labels.keys()))
        self.assertEqual(class_response.name, str(card_ident))
        self.assertEqual(class_response.status, status)
        self.assertEqual(class_response.points, points)
        self.assertEqual(class_response.priority, priority)
        self.assertEqual(class_response.sprint, sprint)

    # Test 3: Issue with bare minimum
    def test_issue_with_minimum(self):
        card_ident = 3
        repo_name = "Repo"
        issue = {"id": f"node_{card_ident}", "type": "ISSUE", "content": {
                                                                     "number": card_ident,
                                                                     "labels": {"nodes": []},
                                                                     "repository": {"name": repo_name}},
                 "fieldValues": {"nodes": []}}
        class_response = CardInfo(issue)
        self.assertEqual(class_response.node_id, f"node_{card_ident}")
        self.assertEqual(class_response.type, "ISSUE")
        self.assertEqual(class_response.id, None)
        self.assertEqual(class_response.number, card_ident)
        self.assertEqual(class_response.repo, repo_name)
        self.assertEqual(class_response.name, str(card_ident))
        self.assertEqual(class_response.labels, [])
        self.assertEqual(class_response.status, None)
        self.assertEqual(class_response.points, 0)
        self.assertEqual(class_response.sprint, None)

    # Test 4: DRAFT_ISSUE
    def test_draft_issue(self):
        card_ident = 4
        class_response = CardInfo(draft_issue_entry(card_ident, {}))
        self.assertEqual(class_response.node_id, f"node_{card_ident}")
        self.assertEqual(class_response.type, "DRAFT_ISSUE")
        self.assertEqual(class_response.id, f"draft_{card_ident}")
        self.assertEqual(class_response.number, f"Draft issue {card_ident}")
        self.assertEqual(class_response.repo, "draft")
        self.assertEqual(class_response.name, f"Draft issue {card_ident}")

    # Test 5: PULL_REQUEST
    def test_pull_request(self):
        card_ident = 5
        class_response = CardInfo(pull_request_entry(card_ident, {}))
        self.assertEqual(class_response.node_id, f"node_{card_ident}")
        self.assertEqual(class_response.type, "PULL_REQUEST")
        self.assertEqual(class_response.id, None)
        self.assertEqual(class_response.number, None)
        self.assertEqual(class_response.repo, None)
        self.assertEqual(class_response.name, "None")

class TestProjectIncrement(TestCase):
    # Test 1: There's an X in the title
    @requests_mock.mock()
    def test_x_in_title(self,m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        title = "PI_2020_02X"
        test_class = ProjectIncrement(0, 0, title, "Org")
        self.assertEqual(test_class.title, title + " is not a Program Increment")
        self.assertEqual(test_class.year, "2000")
        self.assertEqual(test_class.month, "01")

    # Test 2: Not a PI Title
    @requests_mock.mock()
    def test_not_a_pi(self,m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        title = "Example"
        test_class = ProjectIncrement(0, 0, title, "Org")
        self.assertEqual(test_class.title, title + " is not a Program Increment")
        self.assertEqual(test_class.year, "2000")
        self.assertEqual(test_class.month, "01")

    # Test 3: PI in Title but no date
    @requests_mock.mock()
    def test_incorrectly_named_pi(self,m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        title = "PI_2020A_02A"
        test_class = ProjectIncrement(0, 0, title, "Org")
        self.assertEqual(test_class.title, title + " is not a Program Increment")
        self.assertEqual(test_class.year, "2000")
        self.assertEqual(test_class.month, "01")

    # Test 4: PI in Title with date
    @requests_mock.mock()
    def test_correctly_named_pi(self,m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        title = "PI_2020_02"
        test_class = ProjectIncrement(0, 0, title, "Org")
        self.assertEqual(test_class.title, title)
        self.assertEqual(test_class.year, "2020")
        self.assertEqual(test_class.month, "02")


    # Test 5: Returned string
    @requests_mock.mock()
    def test_returned_string(self, m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        title = "PI_2020_01"
        expected_string = "This is project increment: " + title
        test_class = ProjectIncrement(0, 0, title, "Org")
        self.assertEqual(str(test_class), expected_string)

    # Test 6: Get sprints and statuses
    @requests_mock.mock()
    def test_get_sprints_and_statuses(self, m):
        default_pi = PiDefaultResponseValues()
        m.post(url, text=default_pi.response, status_code=200)
        test_class = ProjectIncrement(0, 0, "Example", "Org")
        self.assertEqual(test_class.sprint_field_id, default_pi.sprint_field_id)
        self.assertEqual(test_class.status_field_id, default_pi.status_field_id)
        self.assertEqual(test_class.points_field_id, default_pi.points_field_id)
        self.assertDictEqual(test_class.sprint_ids, default_pi.sprints)
        self.assertDictEqual(test_class.status_ids, default_pi.statuses)
        self.assertEqual(test_class.first_sprint, default_pi.first_sprint)
        self.assertEqual(test_class.last_sprint, default_pi.last_sprint)
    
class TestRepoInfo(TestCase):
    @requests_mock.mock()
    def test_repo_info(self,m):
        repo_name = "repo_name"
        expected_labels = {"label_1": "label_1_id", "label_2": "label_2_id", "label_3": "label_3_id"}
        m.post(url, text=build_response(QlCommand.findRepoInfo, repo_name=repo_name, expected_labels=expected_labels),
               status_code=200)
        test_class = RepoInfo("Org", repo_name)
        self.assertEqual(test_class.name, repo_name)
        self.assertEqual(test_class.labels, expected_labels)

class TestSprintInfo(TestCase):
    # Test 1 - Sprint of format Next PI (2020_04_04)
    def test_sprint_in_next_pi(self):
        sprint_name = "Next PI (2021_01_01)"
        sprint_id = "sprint_id"
        sprint = {"name": sprint_name, "id": sprint_id}
        test_class = SprintInfo(sprint)
        self.assertEqual(test_class.sprint_name, "2021_01_01")
        self.assertTrue(test_class.in_next_pi)
        self.assertEqual(test_class.sprint_year, "2021")
        self.assertEqual(test_class.sprint_month, "01")
        self.assertEqual(test_class.sprint_day, "01")
        self.assertEqual(test_class.sprint_id, sprint_id)
        self.assertEqual(test_class.sprint_start_date, datetime.datetime(2021,1,1,0,0))
        self.assertEqual(str(test_class), str(datetime.datetime(2021,1,1,0,0)))


    # Test 2 - Standard sprint 2020_01_01
    def test_standard_sprint_name(self):
        sprint_name = "2021_02_02"
        sprint_id = "sprint_id"
        sprint = {"name": sprint_name, "id": sprint_id}
        test_class = SprintInfo(sprint)
        self.assertEqual(test_class.sprint_name, sprint_name)
        self.assertFalse(test_class.in_next_pi)
        self.assertEqual(test_class.sprint_year, "2021")
        self.assertEqual(test_class.sprint_month, "02")
        self.assertEqual(test_class.sprint_day, "02")
        self.assertEqual(test_class.sprint_id, sprint_id)
        self.assertEqual(test_class.sprint_start_date, datetime.datetime(2021,2,2,0,0))
        self.assertEqual(str(test_class), str(datetime.datetime(2021,2,2,0,0)))

    # Test 3 - Not a date
    def test_incorrect_name(self):
        sprint_name = "Not a sprint"
        sprint_id = "sprint_id"
        sprint = {"name": sprint_name, "id": sprint_id}
        test_class = SprintInfo(sprint)
        self.assertEqual(test_class.sprint_name, sprint_name)
        self.assertFalse(test_class.in_next_pi)
        self.assertEqual(test_class.sprint_year, "Not ")
        self.assertEqual(test_class.sprint_month, " s")
        self.assertEqual(test_class.sprint_day, "rint")
        self.assertEqual(test_class.sprint_id, sprint_id)
        self.assertEqual(test_class.sprint_start_date, datetime.datetime(2020,1,1,0,0))
        self.assertEqual(str(test_class), str(datetime.datetime(2020,1,1,0,0)))
