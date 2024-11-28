import graph_ql_interactions.graph_ql_functions as gql_queries

repo_label_id_query = gql_queries.open_graph_ql_query_file("findRepoLabelID.txt")
repo_info_query = gql_queries.open_graph_ql_query_file("findRepoInfo.txt")


def get_label_id(org_name="", repo_name="", label_name=""):
    result = gql_queries.run_query(repo_label_id_query.
                                   replace("<ORG_NAME>", org_name).
                                   replace("<REPO>", repo_name).
                                   replace("<LABEL_NAME>", label_name))
    try:
        label_id = result["data"]["repository"]["label"]["id"]
    except TypeError:
        label_id = "NONE_NONE"
    return label_id


def get_repo_labels(org_name="", repo_name=""):
    labels = {}
    repos_query = gql_queries.open_graph_ql_query_file("findRepoInfo.txt")
    result = gql_queries.run_query(repos_query.replace("<ORG_NAME>", org_name).replace("<REPO>", repo_name))
    for entry in result["data"]["repository"]["labels"]["nodes"]:
        labels[entry["name"]] = entry["id"]
    return labels
