# app.py

from flask import Flask, request, abort
import get_project_info
import update_item_info

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        # print(request.json["action"])
        match request.json["action"]:
            case "unlabeled":
                print("Label removed: ", request.json["label"]["name"])
            case "labeled":
                label_added(request.json)
                print("Label added: ", request.json["label"]["name"])
            case "edited":
                # nothing to do here yet
                pass
            case _:
                # print("Data received from Webhook is: ", request.json)
                print("No cases for action: ", request.json["action"])
        return 'success', 200
    else:
        abort(400)


def label_added(info):
    print("Label Added function")
    print(request.json)
    print("Yes, the label added is: ", request.json["label"]["name"])
    print("The issue ID is: ", request.json["issue"]["node_id"])
    print("And the current project number is:", current_project.project_number)
    current_issue = update_item_info.IssueToUpdate(request.json["issue"]["node_id"])
    current_issue.set_project(current_project)
    label_name = request.json["label"]["name"]
    match label_name:
        case "proposal":
            print("Proposed ticket being added to project in next sprint")
            current_issue.place_in_next_sprint()
        case _:
            print("Nothing to be done with this label: ", label_name)


def get_projects():
    print("get_projects")


if __name__ == '__main__':
    current_project = get_project_info.ProjectInfo(True)
    app.run()