# app.py

from flask import Flask, request, abort
import get_project_info
import update_item_info

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        #print(request.json["action"])
        match request.json["action"]:
            case "unlabeled":
                print("Label removed: ", request.json["label"]["name"])
            case "labeled":
                label_added(request.json)
            case "edited":
                print("Something has been edited, I need to allow for this")
                # print(request.json)
                match request.json["changes"]["field_value"]["field_name"]:
                    case "Labels":
                        print("Labels are handled already")
                    case "Status":
                        print("This is the one I want to action, a status change")
                    case _:
                        print("Nothing decided yet for: " + request.json["changes"]["field_value"]["field_name"])
            case _:
                # print("Data received from Webhook is: ", request.json)
                print("No cases for action: ", request.json["action"])
        return 'success', 200
    else:
        abort(400)


def label_added(info):
    print("Label added: ", info["label"]["name"])
    #print("Label Added function")
    #print(request.json)
    #print("Yes, the label added is: ", request.json["label"]["name"])
    #print("The issue ID is: ", request.json["issue"]["node_id"])
    #print("And the current project number is:", current_project.project_number)
    current_issue = update_item_info.IssueToUpdate(info["issue"]["node_id"])
    current_issue.set_project(current_project)
    label_name = info["label"]["name"]
    match label_name:
        case "proposal":
            print("Proposed ticket being added to project in next sprint")
            current_issue.place_in_next_sprint()
        case "added during sprint":
            current_issue.place_in_current_sprint()
        case "in progress":
            current_issue.set_status(current_issue.project_to_use.status_ids["In Progress"])
        case "impeded":
            current_issue.set_status(current_issue.project_to_use.status_ids["Impeded"])
        case "review":
            current_issue.set_status(current_issue.project_to_use.status_ids["Review"])
        case "rework":
            current_issue.set_status(current_issue.project_to_use.status_ids["Backlog"])
        case _:
            print("Nothing to be done with this label: ", label_name)


def get_projects():
    print("get_projects")


if __name__ == '__main__':
    current_project = get_project_info.ProjectInfo(True)
    app.run()