import graph_ql_interactions.graph_ql_functions as gql_queries
from collections import Counter

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
        cards_in_project.append(node)
    # Add items from any further pages
    while has_next_page:
        end_cursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
        result = gql_queries.run_query(card_info_query.
                                       replace("<ORG_NAME>", org_name).
                                       replace("<PROJ_NUM>", str(project_number)).
                                       replace("<AFTER>", "\"" + end_cursor + "\""))
        has_next_page = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
        for node in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
            cards_in_project.append(node)

    return cards_in_project


def get_cards_with_field_values_in_sprint(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)
    # Get the cards in this sprint
    cards_in_sprint = []
    for card in cards_in_project:
        # Split to a further iterable
        field_values = card["fieldValues"]["nodes"]
        for value in field_values:
            try:
                if value["field"]["name"] == "Sprint" and value["name"] == sprint:
                    # Get rid of empty values
                    cards_in_sprint.append([i for i in field_values if i])
            except KeyError:
                # Section is empty ignore it
                pass
    return cards_in_sprint


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
        # Get the labels on the card
        labels = []
        try:
            for label in card["content"]["labels"]["nodes"]:
                labels.append(label["name"])
        except KeyError:
            # Section is empty ignore it
            pass
        # Get the sprint, status and points
        field_values = card["fieldValues"]["nodes"]
        card_points = 0
        card_status = None
        card_sprint = None
        for value in field_values:
            try:
                match value["field"]["name"]:
                    case "Sprint":
                        card_sprint = value["name"]
                    case "Points":
                        card_points = value["number"]
                    case "Status":
                        card_status = value["name"]
                    case _:
                        pass
            except KeyError:
                pass

        if card_sprint == sprint:
            match card_status:
                case "Backlog":
                    snapshot["ready"]["count"] += 1
                    snapshot["ready"]["points"] += card_points
                    if "rework" in labels:
                        snapshot["rework"]["count"] += 1
                        snapshot["rework"]["points"] += card_points
                case "In Progress":
                    snapshot["in_progress"]["count"] += 1
                    snapshot["in_progress"]["points"] += card_points
                case "Impeded":
                    snapshot["impeded"]["count"] += 1
                    snapshot["impeded"]["points"] += card_points
                case "Review":
                    snapshot["review"]["count"] += 1
                    snapshot["review"]["points"] += card_points
                case "Done":
                    snapshot["done"]["count"] += 1
                    snapshot["done"]["points"] += card_points
                case _:
                    # This is not a status I'm interested in, and probably shouldn't exist
                    pass

    return snapshot


def get_number_of_cards_by_status(org_name="", project_number="", sprint=""):
    cards = get_cards_with_field_values_in_sprint(org_name=org_name, project_number=project_number, sprint=sprint)
    card_statuses = []
    for card in cards:
        for value in card:
            try:
                if value["field"]["name"] == "Status":
                    card_statuses.append(value["name"])
            except KeyError:
                # Nothing to worry about this doesn't exist
                pass
    return Counter(card_statuses)


def get_card_ids_in_sprint(org_name="", project_number="", sprint=""):
    cards_in_project = get_cards_in_project(org_name=org_name, project_number=project_number)

    # Get the cards in this sprint
    cards_in_sprint = []
    for card in cards_in_project:
        # Split to a further iterable
        field_values = card["fieldValues"]["nodes"]
        for value in field_values:
            try:
                if value["field"]["name"] == "Sprint" and value["name"] == sprint:
                    # Get rid of empty values
                    cards_in_sprint.append(card["content"]["id"])
            except KeyError:
                # Section is empty ignore it
                pass

    return cards_in_sprint


def add_label(issue_id, label_id_to_add):
    gql_queries.run_query(update_labels.replace("<ISSUE>", issue_id).replace("<LABEL_ID>", label_id_to_add))


def remove_label(issue_id, label_id_to_remove):
    gql_queries.run_query(remove_label_mutation.replace("<ISSUE>", issue_id).replace("<LABEL_ID>", label_id_to_remove))


def get_repo_for_issue(issue_id):
    return gql_queries.run_query(card_repo_query.replace("<ISSUE>", issue_id))["data"]["node"]["repository"]["name"]


get_cards_and_points_snapshot_for_sprint(org_name="Arianiel", project_number="1", sprint="2024_11_01")
