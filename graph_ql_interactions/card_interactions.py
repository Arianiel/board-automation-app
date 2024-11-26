import graph_ql_interactions.graph_ql_functions as gql_queries
from collections import Counter
from github_interactions import card_info

card_info_query = gql_queries.open_graph_ql_query_file("findCardInfo.txt")
update_labels = gql_queries.open_graph_ql_query_file("UpdateItemLabel.txt")
remove_label_mutation = gql_queries.open_graph_ql_query_file("RemoveLabel.txt")
card_repo_query = gql_queries.open_graph_ql_query_file("findIssueRepo.txt")


def get_cards_in_project(org_name="", project_number=""):
    # Note that there should always be at least one page so the pagination is added afterwards
    result = gql_queries.run_query(card_info_query.
                                   replace("<ORG_NAME>", org_name).
                                   replace("<PROJ_NUM>", str(project_number)).
                                   replace("<AFTER>", "null"))
    has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
    cards_in_project = []
    for node in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
        cards_in_project.append(card_info.CardInfo(node))
    # Add items from any further pages
    while has_next_page:
        end_cursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
        result = gql_queries.run_query(card_info_query.
                                       replace("<ORG_NAME>", org_name).
                                       replace("<PROJ_NUM>", str(project_number)).
                                       replace("<AFTER>", "\"" + end_cursor + "\""))
        has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
        for node in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
            cards_in_project.append(card_info.CardInfo(node))

    return cards_in_project


def get_cards_and_points_snapshot_for_sprint(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)
    snapshot = {
        "ready": {"count": 0, "points": 0},
        "rework": {"count": 0, "points": 0},
        "in_progress": {"count": 0, "points": 0},
        "impeded": {"count": 0, "points": 0},
        "review": {"count": 0, "points": 0},
        "done": {"count": 0, "points": 0},
    }
    for card in cards_in_project:
        if card.sprint == sprint:
            match card.status:
                case "Backlog":
                    snapshot["ready"]["count"] += 1
                    snapshot["ready"]["points"] += card.points
                    if "rework" in card.labels:
                        snapshot["rework"]["count"] += 1
                        snapshot["rework"]["points"] += card.points
                case "In Progress":
                    snapshot["in_progress"]["count"] += 1
                    snapshot["in_progress"]["points"] += card.points
                case "Impeded":
                    snapshot["impeded"]["count"] += 1
                    snapshot["impeded"]["points"] += card.points
                case "Review":
                    snapshot["review"]["count"] += 1
                    snapshot["review"]["points"] += card.points
                case "Done":
                    snapshot["done"]["count"] += 1
                    snapshot["done"]["points"] += card.points
                case _:
                    # This is not a status I'm interested in, and probably shouldn't exist
                    pass

    return snapshot


def get_card_list_snapshot_for_sprint(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)
    snapshot = {
        "ready": [],
        "rework": [],
        "in_progress": [],
        "impeded": [],
        "review": [],
        "done": [],
    }
    for card in cards_in_project:
        if card.sprint == sprint:
            match card.status:
                case "Backlog":
                    snapshot["ready"].append({"number": card.number, "repo": card.repo})
                    if "rework" in card.labels:
                        snapshot["rework"].append({"number": card.number, "repo": card.repo})
                case "In Progress":
                    snapshot["in_progress"].append({"number": card.number, "repo": card.repo})
                case "Impeded":
                    snapshot["impeded"].append({"number": card.number, "repo": card.repo})
                case "Review":
                    snapshot["review"].append({"number": card.number, "repo": card.repo})
                case "Done":
                    snapshot["done"].append({"number": card.number, "repo": card.repo})
                case _:
                    # This is not a status I'm interested in, and probably shouldn't exist
                    pass
    return snapshot


def get_planning_snapshot(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)
    snapshot = {
        "high": [],
        "medium": [],
        "low": [],
    }
    for card in cards_in_project:
        if card.sprint == sprint:
            match card.priority:
                case "High":
                    snapshot["high"].append({"number": card.number, "repo": card.repo})
                case "Medium":
                    snapshot["medium"].append({"number": card.number, "repo": card.repo})
                case "Low":
                    snapshot["low"].append({"number": card.number, "repo": card.repo})
                case _:
                    # This is not a status I'm interested in, and probably shouldn't exist
                    pass
    return snapshot


def get_number_of_cards_by_status(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)
    card_statuses = []
    for card in cards_in_project:
        if card.sprint == sprint:
            card_statuses.append(card.status)
    return Counter(card_statuses)


def get_card_issue_ids_in_sprint(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)

    # Get the cards in this sprint
    cards_in_sprint = []
    for card in cards_in_project:
        if card.sprint == sprint and card.type == "ISSUE":
            cards_in_sprint.append(card.id)

    return cards_in_sprint


def add_label(issue_id, label_id_to_add):
    gql_queries.run_query(update_labels.replace("<ISSUE>", issue_id).replace("<LABEL_ID>", label_id_to_add))


def remove_label(issue_id, label_id_to_remove):
    gql_queries.run_query(remove_label_mutation.replace("<ISSUE>", issue_id).replace("<LABEL_ID>", label_id_to_remove))


def get_repo_for_issue(issue_id):
    return gql_queries.run_query(card_repo_query.replace("<ISSUE>", issue_id))["data"]["node"]["repository"]["name"]

