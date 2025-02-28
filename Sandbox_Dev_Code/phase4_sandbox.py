# # # # # # # # # from datetime import datetime, timedelta
# # # # # # # # # import numpy as np
# # # # # # # # # import pandas as pd
# # # # # # # # #
# # # # # # # # # # end_date =
# # # # # # # # # last_day = datetime.today() - timedelta(days=8)
# # # # # # # # # end_date = datetime.today() + timedelta(days=8)
# # # # # # # # # start_date = datetime.today() - timedelta(days=15)
# # # # # # # # # print(f"Start Date: {start_date}")
# # # # # # # # # print(f"End Date: {end_date}")
# # # # # # # # # print(f"Last day: {last_day}, the day is {last_day.day}")
# # # # # # # # #
# # # # # # # # # dates_init = []
# # # # # # # # #
# # # # # # # # # for i in range(1, (last_day - start_date).days + 1):
# # # # # # # # #     dates_init.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
# # # # # # # # #
# # # # # # # # # print(dates_init)
# # # # # # # # #
# # # # # # # # # df = pd.DataFrame({"Test": dates_init})
# # # # # # # # #
# # # # # # # # # test = df["Test"]
# # # # # # # # #
# # # # # # # # # print(df)
# # # # # # # # # print("*****Going to the code to fix*****")
# # # # # # # # # dates = df["Test"][0:]
# # # # # # # # # print(dates)
# # # # # # # # #
# # # # # # # # # for i in range(1, (end_date - start_date).days + 1):
# # # # # # # # #     print(f"================={test}")
# # # # # # # # #     dates = np.append(dates, [(last_day + timedelta(days=i)).strftime("%Y-%m-%d")])
# # # # # # # # #
# # # # # # # # # print("*****This is with the additions*****")
# # # # # # # # # print(dates)
# # # # # # # # #
# # # # # # # # # print("**************ARGHGGHGHGHGHGHGHGHG**************")
# # # # # # # # # print(datetime.today())
# # # # # # # # # print(datetime.today().timestamp())
# # # # # # # # # hmmm = "2025-01-23"
# # # # # # # # # print(hmmm)
# # # # # # # # # print(datetime.strptime(hmmm, "%Y-%m-%d"))
# # # # # # # # #
# # # # # # # # # dates = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", ]
# # # # # # # # # print(dates)
# # # # # # # # #
# # # # # # # # # df = pd.DataFrame({"Test": dates})
# # # # # # # # #
# # # # # # # # # print(df)
# # # # # # # # #
# # # # # # # # # print((last_day + timedelta(days=1)))
# # # # # # # # # print((last_day + timedelta(days=1)))
# # # # # # # # # print(datetime.strptime((last_day + timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d"))
# # # # # # # # import json
# # # # # # # # # from httmock import urlmatch, HTTMock
# # # # # # # # #
# # # # # # # # #
# # # # # # # # # # define matcher:
# # # # # # # # # @urlmatch(netloc=r'(.*\.)?google\.com$')
# # # # # # # # # def google_mock(url, request):
# # # # # # # # #     return 'Feeling lucky, punk?'
# # # # # # # # #
# # # # # # # # # # open context to patch
# # # # # # # # # with HTTMock(google_mock):
# # # # # # # # #     # call requests
# # # # # # # # #     r = requests.get('http://google.com/')
# # # # # # # # # print(r.content)  # 'Feeling lucky, punk?'
# # # # # # # #
# # # # # # # # from unittest import TestCase
# # # # # # # # import requests
# # # # # # # # import requests_mock
# # # # # # # # import graph_ql_interactions.graph_ql_functions as ql
# # # # # # # #
# # # # # # # # class Test(TestCase):
# # # # # # # #     # @requests_mock.mock()
# # # # # # # #     # def test_url_testing(self, m):
# # # # # # # #     #     print("The test is being tried")
# # # # # # # #     #     url = "http://test.html"
# # # # # # # #     #     m.get(url, text="mocked")
# # # # # # # #     #     self.assertEquals(requests.get(url).text, "mocked")
# # # # # # # #
# # # # # # # #     test = {"test": "Antinanco"}
# # # # # # # #     url = 'https://api.github.com/graphql'
# # # # # # # #     text = json.dumps(test)
# # # # # # # #     query = "Example"
# # # # # # # #
# # # # # # # #     @requests_mock.mock()
# # # # # # # #     def test_ql_query_pass(self, m):
# # # # # # # #         m.post(self.__class__.url, text=self.__class__.text, status_code=200)
# # # # # # # #         self.assertDictEqual(ql.run_query(self.__class__.query), self.__class__.test)
# # # # # # # #
# # # # # # # #     @requests_mock.mock()
# # # # # # # #     def test_ql_query_fail(self, m):
# # # # # # # #         m.post(self.__class__.url, text=self.__class__.text, status_code=500)
# # # # # # # #         with self.assertRaises(Exception) as context:
# # # # # # # #             ql.run_query(self.__class__.query)
# # # # # # # #         self.assertTrue(self.__class__.query in str(context.exception))
# # # # # # # from unittest.mock import mock_open, patch
# # # # # # # from unittest import TestCase
# # # # # # # import os
# # # # # # #
# # # # # # # def test(filename: str):
# # # # # # #     with open(os.path.join(os.path.dirname(__file__), "graph_ql_queries", filename), "r") as f:
# # # # # # #         output = f.read()
# # # # # # #     return output
# # # # # # #
# # # # # # # class Test(TestCase):
# # # # # # #     @patch('builtins.open', mock_open(read_data="data"))
# # # # # # #     def test_testme(self):
# # # # # # #         result = test("Something")
# # # # # # #         assert result == "data"
# # # # # #
# # # # # #
# # # # # # import graph_ql_interactions.graph_ql_functions as gql_queries
# # # # # # #
# # # # # # # repo_label_id_query = gql_queries.open_graph_ql_query_file("findRepoLabelID.txt")
# # # # # # # def get_label_id(org_name: str = "", repo_name: str = "", label_name: str = ""):
# # # # # # #     result = gql_queries.run_query(repo_label_id_query.
# # # # # # #                                    replace("<ORG_NAME>", org_name).
# # # # # # #                                    replace("<REPO>", repo_name).
# # # # # # #                                    replace("<LABEL_NAME>", label_name))
# # # # # # #     print(result)
# # # # # # #     try:
# # # # # # #         label_id = result["data"]["repository"]["label"]["id"]
# # # # # # #     except TypeError:
# # # # # # #         label_id = "NONE_NONE"
# # # # # # #     return label_id
# # # # # # #
# # # # # # # print(get_label_id("Arianiel", "issues-repo", "duplicate"))
# # # # # # # # result = "{'data': {'repository': {'label': {'id': 'LA_kwDOMZjARM8AAAABr0GyTA'}}}}"
# # # # # # #
# # # # # # # value = "label_id"
# # # # # # # text = f"{{'data': {{'repository': {{'label': {{'id': {value}}}}}}}"
# # # # # # # print(text)
# # # # # #
# # # # # # def get_repo_labels(org_name: str = "", repo_name: str = ""):
# # # # # #     labels = {}
# # # # # #     repos_query = gql_queries.open_graph_ql_query_file("findRepoInfo.txt")
# # # # # #     result = gql_queries.run_query(repos_query.replace("<ORG_NAME>", org_name).replace("<REPO>", repo_name))
# # # # # #     print(result)
# # # # # #     for entry in result["data"]["repository"]["labels"]["nodes"]:
# # # # # #         labels[entry["name"]] = entry["id"]
# # # # # #     return labels
# # # # # #
# # # # # # print(get_repo_labels("Arianiel", "issues-repo"))
# # # # # #
# # # # # # repo_name = "repo_name"
# # # # # # expected_labels = {"label_1": "label_1_id", "label_2": "label_2_id", "label_3": "label_3_id"}
# # # # # # labels_list = []
# # # # # # for entry in expected_labels.keys():
# # # # # #     labels_list.append({"name": entry, "id": expected_labels[entry]})
# # # # # # print(labels_list)
# # # # # # test = {'data': {'repository': {'name': 'repo_name', 'id': 'repo_name', 'labels': {'nodes': labels_list}}}}
# # # # # # print(test)
# # # # #
# # # # # from collections import Counter
# # # # #
# # # # # import graph_ql_interactions.graph_ql_functions as gql_queries
# # # # # from github_interactions import card_info
# # # # #
# # # # # card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
# # # # # update_labels = gql_queries.open_graph_ql_query_file("UpdateItemLabel.txt")
# # # # # remove_label_mutation = gql_queries.open_graph_ql_query_file("RemoveLabel.txt")
# # # # # card_repo_query = gql_queries.open_graph_ql_query_file("findIssueRepo.txt")
# # # # # set_sprint_mutation = gql_queries.open_graph_ql_query_file("UpdateSprintForItemInProject.txt")
# # # # # set_points_mutation = gql_queries.open_graph_ql_query_file("UpdatePointsForItemInProject.txt")
# # # # #
# # # # # def get_cards_in_project(org_name: str = "", project_number: str = ""):
# # # # #     # Note that there should always be at least one page so the pagination is added afterwards
# # # # #     result = gql_queries.run_query(card_info_query.
# # # # #                                    replace("<ORG_NAME>", org_name).
# # # # #                                    replace("<PROJ_NUM>", str(project_number)).
# # # # #                                    replace("<AFTER>", "null"))
# # # # #     print(result)
# # # # #     has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
# # # # #     cards_in_project = []
# # # # #     for node in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
# # # # #         cards_in_project.append(card_info.CardInfo(node))
# # # # #     # Add items from any further pages
# # # # #     while has_next_page:
# # # # #         end_cursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
# # # # #         result = gql_queries.run_query(card_info_query.
# # # # #                                        replace("<ORG_NAME>", org_name).
# # # # #                                        replace("<PROJ_NUM>", str(project_number)).
# # # # #                                        replace("<AFTER>", "\"" + end_cursor + "\""))
# # # # #         has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
# # # # #         for node in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
# # # # #             cards_in_project.append(card_info.CardInfo(node))
# # # # #
# # # # #     return cards_in_project
# # # # #
# # # # # print(get_cards_in_project("Arianiel", "6"))
# # # # # #
# # # # # # all_labels = "{'nodes': [{'name': 'label_1'}, {'name': 'label)2'}]}"
# # # # # # all_field_values = "{'nodes': [{'name': 'status_value', 'field': {'name': 'Status'}}, {'name': 'sprint_value', 'field': {'name': 'Sprint'}, {'name': 'points_value', 'field': {'name': 'Points'}, {'name': 'priority_value', 'field': {'name': 'Planning Priority'}}]}"
# # # # # #
# # # # # # start_string = "{'data': {'organization': {'projectV2': {'items': {'nodes': ["
# # # # # # # issue_node = f"{{'id': 'node_{index}', 'type': 'ISSUE', 'content': {{'id': 'issue_{index}', 'number': {index}, 'labels': {all_labels}, 'repository': {{'name': 'repo_name'}}}}, 'fieldValues': {all_field_values}}}"
# # # # # # # draft_node = f"{{'id': 'node_{index}', 'type': 'DRAFT_ISSUE', 'content': {{'title': 'Draft Issue {index}', 'id': 'draft_{index}', 'fieldValues': {all_field_values}}}}}"
# # # # # # end_cards = "]"
# # # # # # single_page = "'pageInfo': {'endCursor': 'EC', 'startCursor': 'NC', 'hasNextPage': False, 'hasPreviousPage': False}"
# # # # # # page_one = "'pageInfo': {'endCursor': 'EC', 'startCursor': 'NC', 'hasNextPage': True, 'hasPreviousPage': False}"
# # # # # # page_two = "'pageInfo': {'endCursor': 'EC', 'startCursor': 'NC', 'hasNextPage': False, 'hasPreviousPage': True}"
# # # # # #
# # # # # # end_string = "}}}}}"
# # # # # #
# # # # # # def build_cards_mock(number_of_issues: int=1, number_of_drafts: int=1, only_1_page: bool=True, page_number: int=0):
# # # # # #     cards_mock = "{'data': {'organization': {'projectV2': {'items': {'nodes': ["
# # # # # #     for index in range(1, number_of_issues):
# # # # # #         cards_mock += f"{{'id': 'node_{index}', 'type': 'ISSUE', 'content': {{'id': 'issue_{index}', 'number': {index}, 'labels': {all_labels}, 'repository': {{'name': 'repo_name'}}}}, 'fieldValues': {all_field_values}}}"
# # # # # #     for index in range(number_of_issues + 1, number_of_drafts):
# # # # # #         cards_mock += f"{{'id': 'node_{index}', 'type': 'DRAFT_ISSUE', 'content': {{'title': 'Draft Issue {index}', 'id': 'draft_{index}', 'fieldValues': {all_field_values}}}}}"
# # # # # #     cards_mock += "]"
# # # # # #     if only_1_page:
# # # # # #         cards_mock += "'pageInfo': {'endCursor': 'EC', 'startCursor': 'NC', 'hasNextPage': False, 'hasPreviousPage': False}"
# # # # # #     cards_mock += "}}}}}"
# # # # # #     return cards_mock
# # # # # #
# # # # # #
# # # # # # test_string = start_string
# # # # # # for index in range(1, 4):
# # # # # #     test_string += f"{{'id': 'node_{index}', 'type': 'ISSUE', 'content': {{'id': 'issue_{index}', 'number': {index}, 'labels': {all_labels}, 'repository': {{'name': 'repo_name'}}}}, 'fieldValues': {all_field_values}}}"
# # # # # # for index in range(5, 5):
# # # # # #     test_string += f"{{'id': 'node_{index}', 'type': 'DRAFT_ISSUE', 'content': {{'title': 'Draft Issue {index}', 'id': 'draft_{index}', 'fieldValues': {all_field_values}}}}}"
# # # # # # test_string += end_cards
# # # # # # test_string += single_page
# # # # # # test_string += end_string
# # # # # #
# # # # # # print(test_string)
# # # # # #
# # # # # # print(build_cards_mock(4,1))
# # # # #
# # # #
# # # #
# # # # expected_snapshot = {
# # # #             "ready": {"count": 3, "points": 3},
# # # #             "rework": {"count": 1, "points": 1},
# # # #             "in_progress": {"count": 2, "points": 2},
# # # #             "impeded": {"count": 1, "points": 1},
# # # #             "review": {"count": 3, "points": 3},
# # # #             "done": {"count": 4, "points": 4},
# # # #         }
# # # #
# # # # def snapshot_name_to_status_lookup(snapshot_name: str):
# # # #     match snapshot_name:
# # # #         case "ready" | "rework":
# # # #             return "Backlog"
# # # #         case "in_progress":
# # # #             return "In Progress"
# # # #         case "impeded":
# # # #             return "Impeded"
# # # #         case "review":
# # # #             return "Review"
# # # #         case "done":
# # # #             return "Done"
# # # #         case __:
# # # #             return ""
# # # #
# # # #
# # # # for entry in expected_snapshot.keys():
# # # #     for something in range(0,expected_snapshot[entry]["count"]):
# # # #         statuses = {"points": "1", "status": snapshot_name_to_status_lookup(entry)}
# # # #         if entry == "rework":
# # # #             labels = {"rework": "rework_label_id"}
# # # #
# # # # test = 3.0
# # # # print(test)
# # # #
# # # #
# # # expected_snapshot = {
# # #         "ready": [{1, "repo_1"}, {2, "repo_1"}, {1, "repo_2"}, {2, "repo_2"}],
# # #         "rework": [{1, "repo_1"}],
# # #         "in_progress": [{3, "repo_1"}, {4, "repo_1"}],
# # #         "impeded": [{3, "repo_2"}],
# # #         "review": [{4, "repo_2"}, {5, "repo_1"}],
# # #         "done": [{5, "repo_2"}, {6, "repo_3"}],
# # #     }
# # #
# #
# # from collections import Counter
# #
# # import graph_ql_interactions.graph_ql_functions as gql_queries
# # from github_interactions import card_info
# # #
# # # card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
# # # update_labels = gql_queries.open_graph_ql_query_file("UpdateItemLabel.txt")
# # # remove_label_mutation = gql_queries.open_graph_ql_query_file("RemoveLabel.txt")
# # # card_repo_query = gql_queries.open_graph_ql_query_file("findIssueRepo.txt")
# # # set_sprint_mutation = gql_queries.open_graph_ql_query_file("UpdateSprintForItemInProject.txt")
# # # set_points_mutation = gql_queries.open_graph_ql_query_file("UpdatePointsForItemInProject.txt")
# # #
# # #
# # # sprint_list_id_query = gql_queries.open_graph_ql_query_file("findProjectSprints.txt")
# # #
# # # response = gql_queries.run_query(
# # #     sprint_list_id_query.replace("<PROJ_NUM>", "6")
# # #     .replace("<ORG_NAME>", "Arianiel"))
# # #
# # # print(response)
# # #
# # # fields = response["data"]["organization"]["projectV2"]["fields"]["nodes"]
# # # print(fields)
# #
# # import unittest
# # import unittest.mock
# # from unittest import TestCase
# #
# #
# # class Test:
# #     def __init__(self):
# #         self.value = 1
# #         self.increment_value = 1
# #         self.text = "Some text"
# #
# #     def update_value(self):
# #         self.value += self.increment_value
# #
# # from unittest.mock import patch, PropertyMock
# #
# # class MyClass:
# #     def __init__(self):
# #         self.attr = [1, 2, 3]
# #
# # test = MyClass()
# # with patch.object(test, "attr", new_callable=PropertyMock, return_value = [4, 5, 6]):
# #
# #   print(test.attr) # prints [4, 5, 6]
# #
# # print(test.attr) # prints [1, 2, 3]
# #
# # class MiscTest(TestCase):
# #     # def test(self):
# #     #     f = Test()
# #     #     with patch.object(f, 'text', 3):
# #     #         self.assertEqual(f.text, 3)
# #     #     with patch.object(f, 'increment_value', 2):
# #     #         print(f.value)
# #     #         print(f.update_value())
# #     #         print(f.value)
# #     #     print("Outside the with")
# #     #     print(f.value)
# #     #     print(f.update_value())
# #     #     print(f.value)
# #     #
# import unittest
# from unittest.mock import MagicMock, PropertyMock, Mock, patch
# 
# 
# # from datetime import datetime
# # from unittest.mock import Mock
# #
# # # Save a couple of test days
# # wednesday = datetime(year=2025, month=1, day=1)
# # sunday = datetime(year=2025, month=1, day=5)
# #
# # # Mock datetime to control today's date
# # datetime = Mock()
# #
# # def is_weekday():
# #     today = datetime.today()
# #     # Python's datetime library treats Monday as 0 and Sunday as 6
# #     return 0 <= today.weekday() < 5
# #
# # # Mock .today() to return Wednesday
# # datetime.today.return_value = wednesday
# # # Test Wednesday is a weekday
# # assert is_weekday()
# #
# # # Mock .today() to return Sunday
# # datetime.today.return_value = sunday
# # # Test Sunday is not a weekday
# # assert not is_weekday()
# 
# 
# # m = MagicMock()
# # no_attribute = PropertyMock(side_effect=AttributeError)
# # type(m).my_property = no_attribute
# # print(m.my_property)
# 
# # class Foo:
# #     def __init__(self):
# #         self.something = "Something"
# # #
# # #     def method(self):
# # #         print("It's a method")
# # #
# # # def some_function():
# # #     instance = Foo()
# # #     return instance.method()
# # #
# # # with unittest.mock.patch('module.Foo') as mock:
# # #     instance = mock.return_value
# # #     instance.method.return_value = 'the result'
# # #     result = some_function()
# # #     assert result == 'the result'
# 
# class CalledClass:
#     def __init__(self, name):
#         self.name = name
#         print(f"Init called, I am known as {self.name}")
# 
# class CallingClass:
#     def __init__(self):
#         self.known_as = CalledClass("Initia")
# 
#     def update_known_as(self):
#         self.known_as = CalledClass("Updated")
# 
# test = CallingClass()
# #print(test.known_as.name)
# #print(test.known_as)
# test.update_known_as()
# #print(test.known_as.name)
# #print(test.known_as)
# 
# attempt = MagicMock()
# attempt_name = "Turtle"
# attempt.__getattr__("name").side_effect = attempt_name
# 
# print("*************************")
# 
# class MockCalled:
#     def __init__(self, name):
#         print("%%%%%%%%%%%%%%%%%")
#         print(name)
#         self.name = "Mock"
#         
# 
# with unittest.mock.patch("__main__.CalledClass", new=MockCalled):
#     # MockCalled.side_effect = "Here?"
#     test.update_known_as()
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
#     print(test.known_as.name)
#     # print(test.known_as)
# 
# 
# 
# print("£££££££££££££££££££££££")
# 
# m = MagicMock()
# d = {'key_1': 'value'}
# m.__getitem__.side_effect = d.__getitem__
# 
# # dict behaviour
# print(m['key_1']) # => 'value'
# # print(m['key_2']) # => raise KeyError
# # 
# # # mock behaviour
# # m.foo(42)
# # m.foo.assert_called_once_with(43) # => raise AssertionError


from graph_ql_interactions.card_interactions import *
#print(get_cards_in_project("Arianiel", "6"))

#print(get_when_last_commented_created_on_issue("I_kwDOMZjARM6cd1rv"))

import graph_ql_interactions.graph_ql_functions as gql_queries
query = gql_queries.open_graph_ql_query_file("findIssueLabelsAdded.txt")
last_comment_datetime = gql_queries.run_query(query.replace("<ISSUE>", "I_kwDOMZjARM6cd1rv"))
print(last_comment_datetime)

