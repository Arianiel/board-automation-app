import graph_ql_interactions.graph_ql_functions as gql_queries


class RepoInfo:
    def __init__(self, org_name, repo_name):
        repos_query = gql_queries.open_graph_ql_query_file("findRepoInfo.txt")
        result = gql_queries.run_query(repos_query.replace("<ORG_NAME>", org_name).replace("<REPO>", repo_name))
        print(result)
        self.name = repo_name
        self.labels = {}
        for entry in result["data"]["repository"]["labels"]["nodes"]:
            self.labels[entry["name"]] = entry["id"]
