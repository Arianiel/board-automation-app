import os
import requests

headers = {"Authorization": "token "+open(os.path.join(os.path.dirname(__file__),"..", "config_info","classic_token"), "r").read(),
           'Content-Type': 'application/json'}


def open_graph_ql_query_file(filename):
    with open(os.path.join(os.path.dirname(__file__), "graph_ql_queries", filename), "r") as f:
        output = f.read()
    return output


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

