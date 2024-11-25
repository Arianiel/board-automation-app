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
    # Get the cards in this sprint
    cards_in_sprint = []
    ready_count = 0
    ready_points = 0
    rework_count = 0
    rework_points = 0
    in_progress_count = 0
    in_progress_points = 0
    impeded_count = 0
    impeded_points = 0
    review_count = 0
    review_points = 0
    done_count = 0
    done_points = 0
    for card in cards_in_project:
        print(card)
        labels = []
        try:
            for label in card["content"]["labels"]["nodes"]:
                labels.append(label["name"])
        except KeyError:
            # Section is empty ignore it
            pass
        # Split to a further iterable
        field_values = card["fieldValues"]["nodes"]
        # Find the points
        card_points = 0
        for value in field_values:
            try:
                if value["field"]["name"] == "Points":
                    card_points = value["number"]
                if value["field"]["name"] == "Status":
                    card_status = value["name"]
            except KeyError:
                pass
        print("Card points: ", card_points)
        print("Card status: ", card_status)
        for value in field_values:
            try:
                if value["field"]["name"] == "Sprint" and value["name"] == sprint:
                    # Get rid of empty values
                    cards_in_sprint.append([i for i in field_values if i])
                    if "rework" in labels:
                        rework_count = rework_count + 1
                        rework_points = rework_points + card_points
                    match card_status:
                        case "Backlog":
                            ready_count = ready_count + 1
                            ready_points = ready_points + card_points
                        case "In Progress_":
                            in_progress_count = in_progress_count + 1
                            in_progress_points = in_progress_points + card_points
                        case "Impeded":
                            impeded_count = impeded_count + 1
                            impeded_points = impeded_points + card_points
                        case "Review":
                            review_count = review_count + 1
                            review_points = review_points + card_points
                        case "Done":
                            done_count = done_count + 1
                            done_points = done_points + card_points
                        case _:
                            print("Not matching ", card_status)
            except KeyError:
                # Section is empty ignore it
                pass
    print("Points, etc.")
    print("Ready: number = ", ready_count, "; points = ", ready_points)
    print("Rework: number = ", rework_count, "; points = ", rework_points)
    print("In Progress: number = ", in_progress_count, "; points = ", in_progress_points)
    print("Impeded: number = ", impeded_count, "; points = ", impeded_points)
    print("Review: number = ", review_count, "; points = ", review_points)
    print("Done: number = ", done_count, "; points = ", done_points)
    return cards_in_sprint


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


print(get_cards_and_points_snapshot_for_sprint(org_name="Arianiel", project_number="1", sprint="2024_11_01"))
