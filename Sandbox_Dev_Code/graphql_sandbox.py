import datetime

from github_interactions import get_project_info
import graph_ql_interactions.graph_ql_functions as ql
from collections import Counter
from github_interactions.sprint_information import SprintInfo
import graph_ql_interactions.card_interactions as cards
import graph_ql_interactions.repo_interactions as repos

"""
current_project = get_project_info.ProjectInfo(True)
print(current_project.user_name)
print(current_project.orgs)
print(current_project.org_name)
print(current_project.result_projects)
print(current_project.project_id)
print(current_project.fields)
print(current_project.sprints)

print("--------------")

fields = current_project.fields
sprints = current_project.sprints

print("current_sprint: "+current_project.current_sprint)
print("next_sprint: "+current_project.next_sprint)

current_project = get_project_info.ProjectInfo(True)
print(current_project.status_ids)
print(current_project.status_ids["Backlog"])
label_added = "proposal"
issue_id = "I_kwDOMZjARM6QZUHK"
current_issue = up_info.IssueToUpdate(issue_id)
current_issue.set_project(current_project)

match label_added:
    case "proposal":
        print("Proposed ticket being added to project in next sprint")
        current_issue.place_in_next_sprint()
    case _:
        print("Nothing to be done with this label: ", label_added)
"""

#Add a label
check_repos = """
query ReposInProject {
  organization(login: "Arianiel"){
    login
    	projectV2(number: 1) {
      	title
      	id
      	repositories (first: 5) {
          nodes {
            ... on Repository {
                name
                id
                labels (first: 5) {
                    nodes {
                        name
                        id
                    }
                }
            }
          }
        }
    }
  }
}
"""


check_repos = """
query findProjectSprints
{
    organization(login: "Arianiel"){
        projectV2(number: 1){
            ... on ProjectV2 {
                repositories(first: 5) {
                    nodes {
                        ... on Repository {
                            id
                        }
                    }
                }
                
                fields(first: 20) {
                    nodes {
                        ... on ProjectV2Field {
                            name
                            id
                        }
                        ... on ProjectV2SingleSelectField {
                            name
                            id
                            options {
                                name
                                id
                            }
                        }
                    }
                }
            }
        }
    }
}
"""


check_repos = """
query getIssueRepo {
  node(id: "I_kwDOMZjARM6U3OLH") {
    ... on Issue {
      number
      id
      repository {
        name
      }
    }
  }
}
"""

#print(ql.run_query(check_repos))

add_label = """
mutation UpdateItemLabels {
    addLabelsToLabelable(input: {
        labelableId: "I_kwDOMZjARM6U3OLH",
        labelIds: ["LA_kwDOMZjARM8AAAABr0GyUA"]
    })
    {
        clientMutationId
    }
}
"""

#print(ql.run_query(add_label))
"""
current_project = get_project_info.ProjectInfo(True)
print(current_project.repos)
current_project.add_repo("Test 1")
print(current_project.repos)
current_project.add_repo("Test 2")
print(current_project.repos)
current_project.add_repo("Test 3")
print(str(current_project.repos))

for entry in current_project.repos.keys():
    print(current_project.repos[entry])

testing = ["Test 2", "Test 4"]

for item in testing:
    if item not in current_project.repos.keys():
        print(item + " is not in there")
        current_project.add_repo(item)
    else:
        print(item + " is there")

for entry in current_project.repos.keys():
    print(current_project.repos[entry])
"""


# Check on a repo
query = """
query findRepoInfo {
  repository(owner: "Arianiel", name: "issues-repo") {
    name
    id
    labels(first: 100){
      nodes {
        name
        id
      }
    }
  }
}
"""

# print(ql.run_query(query))
# current_project = get_project_info.ProjectInfo()
# current_project.add_repo("issues-repo")

#print(current_project.repos["issues-repo"].labels["bug"])

add_label = """
mutation UpdateItemLabels {
    addLabelsToLabelable(input: {
        labelableId: "I_kwDOMZjARM6QZUHK",
        labelIds: ["LA_kwDOMZjARM8AAAABr0GyRQ"]
    })
    {
        clientMutationId
    }
}
"""


drop_label = """
mutation RemoveItemLabels {
    removeLabelsFromLabelable(input: {
        labelableId: "I_kwDOMZjARM6QZUHK",
        labelIds: ["LA_kwDOMZjARM8AAAABr0GyRQ"]
    })
    {
        clientMutationId
    }
}
"""
#print(ql.run_query(ql.open_graph_ql_query_file("UpdateItemLabel.txt").replace("<ISSUE>", "I_kwDOMZjARM6QZUHK").replace("<LABEL_ID>", "LA_kwDOMZjARM8AAAABtsil1A")))


query = """
query findCardCounts {
	organization(login: "ISISComputingGroup"){
    projectV2(number: 20){
      title
    }
  }
}
"""


query = """
query findCardInfo {
    organization(login: "ISISComputingGroup"){
        projectV2(number: 20){
            ... on ProjectV2 {
                items(first: 100){
                    nodes {
                        ... on ProjectV2Item{
                            fieldValues(first: 10) {
                                nodes {
                                    ... on ProjectV2ItemFieldSingleSelectValue {
                                        name
                                        field {
                                            ... on ProjectV2SingleSelectField {
                                                name
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

"""

query1 = """
query {
  node(id: "PVTI_lADOAHkvXM4Akjg1zgQzo3k") {
    ... on Issue {
      number
      id
      repository {
        name
      }
    }
  }
}
"""
"""
fields_to_count = ["Backlog", "In Progress"]
current_sprint = "2024_09_05"

result = ql.run_query(query)
print(result)

card_statuses = []

refined_cards = {}
cards_to_refine = []

items = result["data"]["organization"]["projectV2"]["items"]["nodes"]
for item in items:
    field_values = item["fieldValues"]["nodes"]
    for value in field_values:
        try:
            if value["field"]["name"] == "Sprint" and value["name"] == current_sprint:
                cards_to_refine.append([i for i in field_values if i])
        except KeyError:
            # Section is empty ignore it
            pass
        # try:
        #     print(value["name"])
        # except KeyError:
        #     # Section is empty ignore it
        #     pass


    # for value in item["fieldValues"]["nodes"]:
    #     try:
    #         if value["name"] in fields_to_count:
    #             status = value["name"]
    #     except:
    #         # Nothing to
    #     try:
    #         if value["name"] == current_sprint:
    #             print("I WILL BE COUNTING THIS ONE - it is", status)
    #     except KeyError:
    #         # Nothing to do if no data
    #         pass

print(cards_to_refine)

for card in cards_to_refine:
    print(card)
    status = ""
    for value in card:
        print(value)
        try:
            print(value["field"]["name"])
            if value["field"]["name"] == "Status":
                card_statuses.append(value["name"])
        except KeyError:
            # Nothing to worry about this doesn't exist
            pass

print(card_statuses)
card_frequency = Counter(card_statuses)
print(card_frequency)

today = datetime.datetime.today().strftime("%Y-%m-%d")
print(today)

entry_list = [today, ",", str(card_frequency["Backlog"]), ",", str(card_frequency["In Progress"]), ",",
              str(card_frequency["Impeded"]), ",", str(card_frequency["Review"]), ",", str(card_frequency["Done"]), "\r\n"]
entry = "".join(entry_list)

print(entry)

with open("burndown-points.csv", "a") as f:
    f.write(entry)


#current_project = get_project_info.ProjectInfo()
#current_project.current_burndown.update_display()

card_info_query = ql.open_graph_ql_query_file("findCardInfo.txt")
result = ql.run_query(card_info_query.replace("<ORG_NAME>", "ISISComputingGroup").replace("<PROJ_NUM>", str(20)).replace("<AFTER>", "null"))
#print(result)
#print(result["data"]["organization"]["projectV2"]["items"]["pageInfo"])

startCursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["startCursor"]
hasNextPage = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
hasPreviousPage = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasPreviousPage"]
items = []
for item in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
    items.append(item)
print("There are " + str(len(items)) + " items")

while hasNextPage:
    endCursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
    result = ql.run_query(
        card_info_query.replace("<ORG_NAME>", "ISISComputingGroup").replace("<PROJ_NUM>", str(20)).replace("<AFTER>",
                                                                                                           "\"" + endCursor + "\""))
    #print(result)
    #print(result["data"]["organization"]["projectV2"]["items"]["pageInfo"])
    hasNextPage = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["hasNextPage"]
    #endCursor = result["data"]["organization"]["projectV2"]["items"]["pageInfo"]["endCursor"]
    for item in result["data"]["organization"]["projectV2"]["items"]["nodes"]:
        items.append(item)
    print("There are " + str(len(items)) + " items")
print("There are " + str(len(items)) + " items")

extra = {'fieldValues': {'nodes': [{}, {}, {}, {'name': 'Project/Feature', 'field': {'name': 'Classification'}}, {'name': 'In Progress', 'field': {'name': 'Status'}}]}}
print("There are " + str(len(items)) + " items")
print(type(items))
test = []
for item in items:
    test.append(item)
    print(item)
print("Here are my tests")
print(test)
for thing in test:
    print(thing)

cards_to_refine = []
for item in items:
    # Split to a further iterable
    field_values = item["fieldValues"]["nodes"]
    for value in field_values:
        try:
            if value["field"]["name"] == "Sprint" and value["name"] == "2024_11_28":
                # Get rid of empty values
                cards_to_refine.append([i for i in field_values if i])
        except KeyError:
            # Section is empty ignore it
            pass
print(cards_to_refine)

cards_to_refine = []
for item in test:
    # Split to a further iterable
    field_values = item["fieldValues"]["nodes"]
    for value in field_values:
        try:
            if value["field"]["name"] == "Sprint" and value["name"] == "2024_11_28":
                # Get rid of empty values
                cards_to_refine.append([i for i in field_values if i])
        except KeyError:
            # Section is empty ignore it
            pass
print(cards_to_refine)


items = result["data"]["organization"]["projectV2"]["items"]["nodes"]
for item in items:
    print(item)
"""

# current_project = get_project_info.ProjectInfo()
# print(current_project.user_name)
# print(current_project.orgs)
# print(current_project.org_name)
# print(current_project.result_projects)
# print(current_project.project_id)
# print(current_project.fields)
# print(current_project.sprint_ids)
#

"""
today = datetime.datetime.today()
today_day = today.strftime("%d")
today_month = today.strftime("%m")
today_year = today.strftime("%Y")
today = datetime.datetime(year=int(today_year), month=int(today_month), day=int(today_day))

sprint_list_id_query = ql.open_graph_ql_query_file("findProjectSprints.txt")

fields = ql.run_query(
    sprint_list_id_query.replace("<PROJ_NUM>", "1")
    .replace("<ORG_NAME>", "Arianiel"))["data"]["organization"]["projectV2"]["fields"]["nodes"]

print(fields)

sprints = {}
sprint_ids = {}
sprint_by_class = {}
status_ids = {}
for field in fields:
    match field["name"]:
        case "Sprint":
            print("These are my sprints")
            print(field)
            sprint_field_id = field["id"]
            for option in field["options"]:
                print("The option I have is: " + option["name"])
                sprint_ids[option["name"]] = option["id"]
                sprint_by_class[option["name"]] = SprintInfo(option)
        case "Status":
            status_field_id = field["id"]
            for option in field["options"]:
                status_ids[option["name"]] = option["id"]
        case _:
            print(field["name"] + " not found, doing nothing")
print("Setting up my sprint information")
print(sprint_ids)
print(sprint_by_class["2024_10_01"])

current_sprint = ""
next_sprint = ""

for sprint in sprint_by_class.keys():
    if sprint_by_class[sprint] == today:
        current_sprint = sprint
    if sprint_by_class[sprint].sprint_start_date < today:
        try:
            if sprint_by_class[current_sprint].sprint_start_date < \
                    sprint_by_class[sprint].sprint_start_date:
                current_sprint = sprint
        except KeyError:
            current_sprint = sprint
    if sprint_by_class[sprint].sprint_start_date > today:
        try:
            if (sprint_by_class[next_sprint].sprint_start_date > sprint_by_class[sprint].
                    sprint_start_date):
                next_sprint = sprint
        except KeyError:
            next_sprint = sprint

print(current_sprint)
print(next_sprint)
"""


current_project = get_project_info.ProjectInfo()
#cards_to_refine = cards.get_cards_with_field_values_in_sprint(org_name=current_project.org_name, project_number=current_project.project_number, sprint=current_project.current_sprint)
#for card in cards_to_refine:
#    print(card)
cards_to_refine = cards.get_card_ids_in_sprint(org_name=current_project.org_name, project_number=current_project.project_number, sprint=current_project.current_sprint)
for card in cards_to_refine:
    #cards.remove_label(card, current_project.repos[cards.get_repo_for_issue(card)].labels["proposal"])
    #current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["review"])
    repo = cards.get_repo_for_issue(card)
    print(card)
    print(repo)
    label_id = repos.get_label_id(org_name=current_project.org_name, repo_name=repo, label_name="proposal")
    print(label_id)
    cards.remove_label(card, repos.get_label_id(org_name=current_project.org_name, repo_name=cards.get_repo_for_issue(card), label_name="proposal"))
