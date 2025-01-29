import json
from enum import Enum, auto

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
        fields.append({'name': entry, 'field': {'name': expected_fields[entry]}})
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
    
    # The below should allow for extended testing for multiple pages, but this is not considered a necessary test at 
    # this point
    has_next = False
    has_previous = False        
    page_info = {"endCursor": "EC", "startCursor": "NC", "hasNextPage": has_next, "hasPreviousPage": has_previous}
            
    cards_mock = {"data": {"organization": {"projectV2": {"items": {"nodes": issues, "pageInfo": page_info}}}}}
    return cards_mock

def build_response(ql_command: QlCommand, **kwargs):
    match ql_command:
        case QlCommand.findRepoLabelId:
            response = {"data": {"repository": {"label": {"id": kwargs["expected_label_id"]}}}}
        case QlCommand.findRepoInfo:
            response = {'data': {'repository': {'name': kwargs["repo_name"], 'id': kwargs["repo_name"],
                                    'labels': {'nodes': labels_list(kwargs["expected_labels"])}}}}
        case QlCommand.findCardInfo:
            response = build_cards_simple(kwargs["number_of_issues"], 0, True)
        case __:
            response = ""
    return json.dumps(response)

