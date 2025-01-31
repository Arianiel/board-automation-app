from collections import Counter
from unittest import TestCase
import graph_ql_interactions.graph_ql_functions as ql
import graph_ql_interactions.repo_interactions as ri
import graph_ql_interactions.card_interactions as ci
import requests_mock
from unittest.mock import mock_open, patch
from test_helpers import *

# The URL to be mocked here is always the GitHub graphQL API
url = 'https://api.github.com/graphql'

class TestRepoInteractions(TestCase):
    @requests_mock.mock()
    def test_get_label_id_good(self, m):
        value = "label_id"
        m.post(url, text=build_response(QlCommand.findRepoLabelId, expected_label_id=value), status_code=200)
        self.assertEqual(ri.get_label_id("org_name", "repo_name", "label_name"), value)

    @requests_mock.mock()
    def test_get_label_id_bad(self, m):
        value = "NONE_NONE" # This is a magic value from the code
        m.post(url, text=bad_return(), status_code=200)
        self.assertEqual(ri.get_label_id("org_name", "repo_name", "label_name"), value)

    @requests_mock.mock()
    def test_get_repo_labels(self, m):
        repo_name = "repo_name"
        expected_labels = {"label_1": "label_1_id", "label_2": "label_2_id", "label_3": "label_3_id"}        
        m.post(url, text=build_response(QlCommand.findRepoInfo, repo_name=repo_name, expected_labels=expected_labels), 
               status_code=200)
        self.assertEqual(ri.get_repo_labels("org_name", repo_name), expected_labels)
        

class TestGraphQlFunctions(TestCase):
    @patch('builtins.open', mock_open(read_data="data"))
    def test_open_graph_ql_query_file(self):
        result = ql.open_graph_ql_query_file("Something")
        assert result == "data"
    
    # Values for the run_query class which can be used pass or fail
    test = {"test": "Antinanco"}
    text = json.dumps(test)
    query = "Example"

    @requests_mock.mock()
    def test_ql_query_pass(self, m):
        m.post(url, text=self.__class__.text, status_code=200)
        self.assertDictEqual(ql.run_query(self.__class__.query), self.__class__.test)

    @requests_mock.mock()
    def test_ql_query_fail(self, m):
        m.post(url, text=self.__class__.text, status_code=500)
        with self.assertRaises(Exception) as context:
            ql.run_query(self.__class__.query)
        self.assertTrue(self.__class__.query in str(context.exception))
    
    
class TestCardInteractions(TestCase):
    @requests_mock.mock()
    def test_get_cards_in_project(self, m):
        cards_to_create = 3
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="simple", number_of_issues=cards_to_create), 
               status_code=200)
        self.assertEqual(len(ci.get_cards_in_project("Org", "0")), cards_to_create)

    @requests_mock.mock()
    def test_get_cards_and_points_snapshot_for_sprint(self, m):
        expected_snapshot = {
            "ready": {"count": 3, "points": 3},
            "rework": {"count": 1, "points": 1},
            "in_progress": {"count": 2, "points": 2},
            "impeded": {"count": 1, "points": 1},
            "review": {"count": 3, "points": 3},
            "done": {"count": 4, "points": 4},
        }
        sprint_name = "sprint"
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="points_snapshot", 
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        self.assertDictEqual(ci.get_cards_and_points_snapshot_for_sprint("org_name", "0", sprint_name), expected_snapshot)

    @requests_mock.mock()
    def test_get_card_list_snapshot_for_sprint(self, m):
        expected_snapshot = {
            "ready": [{"number": 1, "repo": "repo_1"}, {"number": 2, "repo": "repo_1"}, {"number": 1, "repo": "repo_2"},
                      {"number": 2, "repo": "repo_2"}],
            "rework": [{"number": 1, "repo": "repo_1"}],
            "in_progress": [{"number": 3, "repo": "repo_1"}, {"number": 4, "repo": "repo_1"}],
            "impeded": [{"number": 3, "repo": "repo_2"}],
            "review": [{"number": 4, "repo": "repo_2"}, {"number": 5, "repo": "repo_1"}],
            "done": [{"number": 5, "repo": "repo_2"}, {"number": 6, "repo": "repo_3"}],
        }
        sprint_name = "sprint"
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="card_list_snapshot",
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        self.assertDictEqual(ci.get_card_list_snapshot_for_sprint("org_name", "0", sprint_name),
                             expected_snapshot)

    @requests_mock.mock()
    def test_get_planning_snapshot(self, m):
        expected_snapshot = {
            "high": [{"number": 1, "repo": "repo_1"}, {"number": 2, "repo": "repo_1"}, {"number": 1, "repo": "repo_2"},
                      {"number": 2, "repo": "repo_2"}],
            "medium": [{"number": 3, "repo": "repo_1"}, {"number": 4, "repo": "repo_1"}],
            "low": [{"number": 3, "repo": "repo_2"}],
        }
        sprint_name = "sprint"
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="card_list_planning",
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        self.assertDictEqual(ci.get_planning_snapshot("org_name", "0", sprint_name),
                             expected_snapshot)

    @requests_mock.mock()
    def test_get_number_of_cards_by_status(self, m):
        expected_snapshot = {
            "ready": {"count": 3, "points": 3},
            "rework": {"count": 1, "points": 1},
            "in_progress": {"count": 2, "points": 2},
            "impeded": {"count": 1, "points": 1},
            "review": {"count": 3, "points": 3},
            "done": {"count": 4, "points": 4},
        }
        alternative = []
        for entry in expected_snapshot:
            for value in range(0, expected_snapshot[entry]["count"]):
                alternative.append(snapshot_name_to_status_lookup(entry))
        sprint_name = "sprint"
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="points_snapshot",
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        self.assertCountEqual(ci.get_number_of_cards_by_status("org_name", "0", sprint_name),
                             Counter(alternative))

    @requests_mock.mock()
    def test_get_card_issue_ids_in_sprint(self, m):
        expected_snapshot = {
            "ready": [{"number": 1, "repo": "repo_1"}, {"number": 2, "repo": "repo_1"}, {"number": 1, "repo": "repo_2"},
                      {"number": 2, "repo": "repo_2"}],
            "rework": [{"number": 1, "repo": "repo_1"}],
            "in_progress": [{"number": 3, "repo": "repo_1"}, {"number": 4, "repo": "repo_1"}],
            "impeded": [{"number": 3, "repo": "repo_2"}],
            "review": [{"number": 4, "repo": "repo_2"}, {"number": 5, "repo": "repo_1"}],
            "done": [{"number": 5, "repo": "repo_2"}, {"number": 6, "repo": "repo_3"}],
        }
        sprint_name = "sprint"
        expected_issues = []
        for entry in expected_snapshot:
            if entry == "rework":
                continue
            for item in expected_snapshot[entry]:
                expected_issues.append(f"issue_{item['number']}")
        m.post(url, text=build_response(QlCommand.findCardInfo, card_type="card_list_snapshot",
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        self.assertEqual(ci.get_card_issue_ids_in_sprint("org_name", "0", sprint_name), expected_issues)
    
    def test_add_label(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_remove_label(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_repo_for_issue(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_set_sprint(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_update_sprint_for_all_open_cards(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_set_points(self):
        # TODO
        # Figure out how to test this!
        pass