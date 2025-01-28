from unittest import TestCase
import graph_ql_interactions.graph_ql_functions as ql
import graph_ql_interactions.repo_interactions as ri
import graph_ql_interactions.card_interactions as ci
import json
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
    def test_get_cards_in_project_single_page(self, m):
        print(build_response(QlCommand.findCardInfo, number_of_issues=2))
        m.post(url, text=build_response(QlCommand.findCardInfo, number_of_issues=2), status_code=200)
        print(ci.get_cards_in_project("Org", "0"))
    
    def test_get_cards_in_project_double_page(self):
        # TODO
        # Figure out how to test this!
        pass
        # TSimple test for multiple pages

    def test_get_cards_and_points_snapshot_for_sprint(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_card_list_snapshot_for_sprint(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_planning_snapshot(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_number_of_cards_by_status(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_card_issue_ids_in_sprint(self):
        # TODO
        # Figure out how to test this!
        pass
    
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