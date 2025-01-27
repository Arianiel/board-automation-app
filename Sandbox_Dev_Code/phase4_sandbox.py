# # # from datetime import datetime, timedelta
# # # import numpy as np
# # # import pandas as pd
# # #
# # # # end_date =
# # # last_day = datetime.today() - timedelta(days=8)
# # # end_date = datetime.today() + timedelta(days=8)
# # # start_date = datetime.today() - timedelta(days=15)
# # # print(f"Start Date: {start_date}")
# # # print(f"End Date: {end_date}")
# # # print(f"Last day: {last_day}, the day is {last_day.day}")
# # #
# # # dates_init = []
# # #
# # # for i in range(1, (last_day - start_date).days + 1):
# # #     dates_init.append((start_date + timedelta(days=i)).strftime("%Y-%m-%d"))
# # #
# # # print(dates_init)
# # #
# # # df = pd.DataFrame({"Test": dates_init})
# # #
# # # test = df["Test"]
# # #
# # # print(df)
# # # print("*****Going to the code to fix*****")
# # # dates = df["Test"][0:]
# # # print(dates)
# # #
# # # for i in range(1, (end_date - start_date).days + 1):
# # #     print(f"================={test}")
# # #     dates = np.append(dates, [(last_day + timedelta(days=i)).strftime("%Y-%m-%d")])
# # #
# # # print("*****This is with the additions*****")
# # # print(dates)
# # #
# # # print("**************ARGHGGHGHGHGHGHGHGHG**************")
# # # print(datetime.today())
# # # print(datetime.today().timestamp())
# # # hmmm = "2025-01-23"
# # # print(hmmm)
# # # print(datetime.strptime(hmmm, "%Y-%m-%d"))
# # #
# # # dates = ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04", ]
# # # print(dates)
# # #
# # # df = pd.DataFrame({"Test": dates})
# # #
# # # print(df)
# # #
# # # print((last_day + timedelta(days=1)))
# # # print((last_day + timedelta(days=1)))
# # # print(datetime.strptime((last_day + timedelta(days=1)).strftime("%Y-%m-%d"), "%Y-%m-%d"))
# # import json
# # # from httmock import urlmatch, HTTMock
# # #
# # #
# # # # define matcher:
# # # @urlmatch(netloc=r'(.*\.)?google\.com$')
# # # def google_mock(url, request):
# # #     return 'Feeling lucky, punk?'
# # #
# # # # open context to patch
# # # with HTTMock(google_mock):
# # #     # call requests
# # #     r = requests.get('http://google.com/')
# # # print(r.content)  # 'Feeling lucky, punk?'
# # 
# # from unittest import TestCase
# # import requests
# # import requests_mock
# # import graph_ql_interactions.graph_ql_functions as ql
# # 
# # class Test(TestCase):
# #     # @requests_mock.mock()
# #     # def test_url_testing(self, m):
# #     #     print("The test is being tried")
# #     #     url = "http://test.html"
# #     #     m.get(url, text="mocked")
# #     #     self.assertEquals(requests.get(url).text, "mocked")
# #     
# #     test = {"test": "Antinanco"}
# #     url = 'https://api.github.com/graphql'
# #     text = json.dumps(test)
# #     query = "Example"
# # 
# #     @requests_mock.mock()
# #     def test_ql_query_pass(self, m):
# #         m.post(self.__class__.url, text=self.__class__.text, status_code=200)
# #         self.assertDictEqual(ql.run_query(self.__class__.query), self.__class__.test)
# # 
# #     @requests_mock.mock()
# #     def test_ql_query_fail(self, m):
# #         m.post(self.__class__.url, text=self.__class__.text, status_code=500)
# #         with self.assertRaises(Exception) as context:
# #             ql.run_query(self.__class__.query)
# #         self.assertTrue(self.__class__.query in str(context.exception))
# from unittest.mock import mock_open, patch
# from unittest import TestCase
# import os
# 
# def test(filename: str):
#     with open(os.path.join(os.path.dirname(__file__), "graph_ql_queries", filename), "r") as f:
#         output = f.read()
#     return output
# 
# class Test(TestCase):
#     @patch('builtins.open', mock_open(read_data="data"))
#     def test_testme(self):
#         result = test("Something")
#         assert result == "data"


import graph_ql_interactions.graph_ql_functions as gql_queries
# 
# repo_label_id_query = gql_queries.open_graph_ql_query_file("findRepoLabelID.txt")
# def get_label_id(org_name: str = "", repo_name: str = "", label_name: str = ""):
#     result = gql_queries.run_query(repo_label_id_query.
#                                    replace("<ORG_NAME>", org_name).
#                                    replace("<REPO>", repo_name).
#                                    replace("<LABEL_NAME>", label_name))
#     print(result)
#     try:
#         label_id = result["data"]["repository"]["label"]["id"]
#     except TypeError:
#         label_id = "NONE_NONE"
#     return label_id
# 
# print(get_label_id("Arianiel", "issues-repo", "duplicate"))
# # result = "{'data': {'repository': {'label': {'id': 'LA_kwDOMZjARM8AAAABr0GyTA'}}}}"
# 
# value = "label_id"
# text = f"{{'data': {{'repository': {{'label': {{'id': {value}}}}}}}"
# print(text)

def get_repo_labels(org_name: str = "", repo_name: str = ""):
    labels = {}
    repos_query = gql_queries.open_graph_ql_query_file("findRepoInfo.txt")
    result = gql_queries.run_query(repos_query.replace("<ORG_NAME>", org_name).replace("<REPO>", repo_name))
    print(result)
    for entry in result["data"]["repository"]["labels"]["nodes"]:
        labels[entry["name"]] = entry["id"]
    return labels

print(get_repo_labels("Arianiel", "issues-repo"))

repo_name = "repo_name"
expected_labels = {"label_1": "label_1_id", "label_2": "label_2_id", "label_3": "label_3_id"}
labels_list = []
for entry in expected_labels.keys():
    labels_list.append({"name": entry, "id": expected_labels[entry]})
print(labels_list)
test = {'data': {'repository': {'name': 'repo_name', 'id': 'repo_name', 'labels': {'nodes': labels_list}}}}
print(test)
