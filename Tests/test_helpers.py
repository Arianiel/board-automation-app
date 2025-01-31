import json
from enum import Enum, auto

from pandas.core.computation.ops import isnumeric


class QlCommand(Enum):
    findCardInfo = auto()
    findIssueRepo = auto()
    findOrgs = auto()
    findProjects = auto()
    findProjectSprints = auto()
    findRepoInfo = auto()
    findRepoLabelId = auto()
    RemoveLabel = auto()
    SetProject = auto()
    UpdateItemLabel = auto()
    UpdatePointsForItemInProject = auto()
    UpdateSprintForItemInProject = auto()
    UpdateStatusForItemInProject = auto()

def bad_return():
    """
    To ensure errors are handled in a known way use this helper
    :return: Something that will not be usable by any code
    """
    return json.dumps("Testing Errors")


def labels_list(expected_labels: {}):
    """
    Formats a list of labels to the correct examples for use via response_mock for the GitHub graphQL API
    :param expected_labels: a dictionary of {"label_name_1": "label_id_1", "label_name_2": "label_id_2", etc.}
    :return: a list of dictionaries of the format [{"name": "label_name_1", "id": "label_id_1"},
                                                   {"name": "label_name_2", "id": "label_id_=2"}, etc.]
    """
    labels = []
    for entry in expected_labels.keys():
        labels.append({"name": entry, "id": expected_labels[entry]})
    return labels

def fields_list(expected_fields: {}):
    """
    Formats a list of labels to the correct examples for use via response_mock for the GitHub graphQL API
    :param expected_fields: a dictionary of {"field_name_1": "field_value_1", "field_name_2": "field_value_2", etc.}
    :return: a list of dictionaries of the format [{'name': 'field_value_1', 'field': {'name': 'field_name_1'}},
                                                   {'name': 'field_value_2', 'field': {'name': 'field_name_2'}}, etc.]
    """
    fields = []
    for entry in expected_fields.keys():
        if isnumeric(type(expected_fields[entry])):
            fields.append({'number': expected_fields[entry], 'field': {'name': entry}})
        else:
            fields.append({'name': expected_fields[entry], 'field': {'name': entry}})
    return fields

def issue_entry(ident: int, labels: {}, fields: {}, repo_name: str):
    issue = {"id": f"node_{ident}", "type": "ISSUE", "content": {"id": f"issue_{ident}",
                                                                 "number": ident,
                                                                 "labels": {"nodes": labels_list(labels)},
                                                                 "repository": {"name": repo_name}},
                                                                 "fieldValues": {"nodes": fields_list(fields)}}
    return issue

def draft_issue_entry(ident: int, fields: {}):
    draft_issue = {"id": f"node_{ident}", "type": "DRAFT_ISSUE", "content": {"title": f"Draft issue {ident}",
                                                                             "id": f"draft_{ident}"},
                                                                             "fieldValues": {"nodes": fields_list(fields)}}
    return draft_issue

def build_cards_simple(number_of_issues: int=1, number_of_drafts: int=1, labels=None, statuses=None,
                       repo_name: str="repo_name"):
    if statuses is None:
        statuses = {"status": "status_value"}
    if labels is None:
        labels = {"label_1": "label_1_id"}
    issues = []
    for index in range(0, number_of_issues):
        issues.append(issue_entry(index + 1, labels, statuses, repo_name))
    for index in range(number_of_issues + 1, number_of_drafts):
        issues.append(draft_issue_entry(index + 1, statuses))
    return build_response_contents(issues)
   
def build_response_contents(issues: [], has_next: bool=False, has_previous: bool=False):
    page_info = {"endCursor": "EC", "startCursor": "NC", "hasNextPage": has_next, "hasPreviousPage": has_previous}
    cards_mock = {"data": {"organization": {"projectV2": {"items": {"nodes": issues, "pageInfo": page_info}}}}}
    return cards_mock

def snapshot_name_to_status_lookup(snapshot_name: str):
    match snapshot_name:
        case "ready" | "rework":
            return "Backlog"
        case "in_progress":
            return "In Progress"
        case "impeded":
            return "Impeded"
        case "review":
            return "Review"
        case "done":
            return "Done"
        case __:
            return ""

def priority_lookup(snapshot_name: str):
    match snapshot_name:
        case "high":
            return "High"
        case "medium":
            return "Medium"
        case "low":
            return "Low"
        case __:
            return ""

def build_points_snapshot_cards(expected_snapshot: {}, sprint_name: str= "sprint"):
    issues = []
    outer_index = 0
    for entry in expected_snapshot.keys():
        outer_index += 10
        target = expected_snapshot[entry]["count"]
        if entry == "ready":
            target = expected_snapshot[entry]["count"] - expected_snapshot["rework"]["count"]
        for index in range(0, target):
            fields = {"Points": 1.0, "Status": snapshot_name_to_status_lookup(entry), "Sprint": sprint_name}
            labels = {entry: f"{entry}_label_id"}
            if entry == "rework":
                labels["rework"] = "rework_label_id"
            issues.append(issue_entry(outer_index + index, labels, fields, "repo_name"))
    return build_response_contents(issues)

def build_card_list_snapshot(expected_snapshot: {}, sprint_name: str= "sprint"):
    issues = []
    for entry in expected_snapshot.keys():
        if entry == "rework":
            continue
        for item in expected_snapshot[entry]:
            fields = {"Status": snapshot_name_to_status_lookup(entry), "Sprint": sprint_name}
            labels = {entry: f"{entry}_label_id"}
            if item in expected_snapshot["rework"]:
                labels["rework"] = "rework_label_id"
            issues.append(issue_entry(item["number"], labels, fields, item["repo"]))
    return build_response_contents(issues)

def build_planning_list_snapshot(expected_snapshot: {}, sprint_name: str= "sprint"):
    issues = []
    for entry in expected_snapshot.keys():
        for item in expected_snapshot[entry]:
            fields = {"Planning Priority": priority_lookup(entry), "Sprint": sprint_name}
            issues.append(issue_entry(item["number"], {}, fields, item["repo"]))
    return build_response_contents(issues)
    
def build_response(ql_command: QlCommand, **kwargs):
    match ql_command:
        case QlCommand.findRepoLabelId:
            response = {"data": {"repository": {"label": {"id": kwargs["expected_label_id"]}}}}
        case QlCommand.findRepoInfo:
            response = {'data': {'repository': {'name': kwargs["repo_name"], 'id': kwargs["repo_name"],
                                    'labels': {'nodes': labels_list(kwargs["expected_labels"])}}}}
        case QlCommand.findCardInfo:
            match kwargs["card_type"]:
                case "simple":
                    response = build_cards_simple(kwargs["number_of_issues"], 0)
                case "points_snapshot":
                    response = build_points_snapshot_cards(kwargs["expected_snapshot"], kwargs["sprint_name"])
                case "card_list_snapshot":
                    response = build_card_list_snapshot(kwargs["expected_snapshot"], kwargs["sprint_name"])
                case "card_list_planning":
                    response = build_planning_list_snapshot(kwargs["expected_snapshot"], kwargs["sprint_name"])
                case __:
                    response = ""
        case QlCommand.findIssueRepo:
            response = {"data": {"node": {"repository": {"name": kwargs["repo_name"]}}}}
        case __:
            response = ""
    return json.dumps(response)

