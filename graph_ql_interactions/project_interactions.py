import graph_ql_interactions.github_request_functions as gql_queries

proj_list_query = gql_queries.open_graph_ql_query_file("findProjects.txt")


def get_projects(org_name: str = ""):
    return gql_queries.run_query(proj_list_query.replace("<ORG_NAME>", org_name))["data"][
        "organization"
    ]["projectsV2"]["nodes"]
