import os
import requests
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config_info","config.ini"))
token = config["GITHUB.INTERACTION"]["token"]

headers = {"Authorization": "token "+token, 'Content-Type': 'application/json'}


def open_graph_ql_query_file(filename):
    with open(os.path.join(os.path.dirname(__file__), "graph_ql_queries", filename), "r") as f:
        output = f.read()
    return output


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

