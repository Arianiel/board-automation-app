import graph_ql_interactions.repo_interactions as repos


class RepoInfo:
    def __init__(self, org_name, repo_name):
        self.name = repo_name
        self.labels = repos.get_repo_labels(org_name=org_name, repo_name=repo_name)
