from unittest import TestCase
import graph_ql_interactions.graph_ql_functions as ql
import json
import requests_mock
from unittest.mock import mock_open, patch

class TestRepoInteractions(TestCase):
    def test_get_label_id(self):
        # TODO
        # Figure out how to test this!
        pass
    
    def test_get_repo_labels(self):
        # TODO
        # Figure out how to test this!
        pass
    
class TestGraphQlFunctions(TestCase):
    @patch('builtins.open', mock_open(read_data="data"))
    def test_open_graph_ql_query_file(self):
        result = ql.open_graph_ql_query_file("Something")
        assert result == "data"
    
    test = {"test": "Antinanco"}
    url = 'https://api.github.com/graphql'
    text = json.dumps(test)
    query = "Example"

    @requests_mock.mock()
    def test_ql_query_pass(self, m):
        m.post(self.__class__.url, text=self.__class__.text, status_code=200)
        self.assertDictEqual(ql.run_query(self.__class__.query), self.__class__.test)

    @requests_mock.mock()
    def test_ql_query_fail(self, m):
        m.post(self.__class__.url, text=self.__class__.text, status_code=500)
        with self.assertRaises(Exception) as context:
            ql.run_query(self.__class__.query)
        self.assertTrue(self.__class__.query in str(context.exception))
    
    
class TestCardInteractions(TestCase):
    def test_get_cards_in_project(self):
        # TODO
        # Figure out how to test this!
        pass

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