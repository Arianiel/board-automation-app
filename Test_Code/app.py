from flask import Flask, request, abort
import get_project_info
import update_item_info

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        match request.json["action"]:
            case "unlabeled":
                print("Label removed, nothing to do: ", request.json["label"]["name"])
            case "labeled":
                label_added(request.json)
            case "edited":
                print("Something has been edited, I need to allow for this")
                match request.json["changes"]["field_value"]["field_name"]:
                    case "Labels":
                        # Labels should already have been handled elsewhere
                        pass
                    case "Status":
                        status_changed(request.json)
                    case _:
                        print("Nothing decided yet for: " + request.json["changes"]["field_value"]["field_name"])
            case _:
                print("No cases for action: ", request.json["action"])
        return 'success', 200
    else:
        abort(400)


def status_changed(info):
    print("Handle a status change")
    if info["projects_v2_item"]["content_type"] == "Issue":
        status_from = info["changes"]["field_value"]["from"]["name"]
        status_to = info["changes"]["field_value"]["to"]["name"]
        current_issue = update_item_info.IssueToUpdate(info["projects_v2_item"]["content_node_id"])
        current_issue.get_repo()
        current_project.add_repo(current_issue.repo_name)
        match status_from:
            case "Done":
                # Nothing to do for Done
                return
            case "In Progress":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["in progress"])
            case "Impeded":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["impeded"])
            case "Review":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["review"])
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["under review"])
            case "Backlog":
                # Nothing to do for Backlog here
                return
            case _:
                print("Nothing planned for going from this status: ", status_from)
        match status_to:
            case "Done":
                # Nothing to do for Done
                return
            case "In Progress":
                current_issue.add_label(current_project.repos[current_issue.repo_name].labels["in progress"])
                if status_from == "Review":
                    current_issue.add_label(current_project.repos[current_issue.repo_name].labels["rework"])
            case "Impeded":
                current_issue.add_label(current_project.repos[current_issue.repo_name].labels["impeded"])
            case "Review":
                current_issue.add_label(current_project.repos[current_issue.repo_name].labels["review"])
            case "Backlog":
                if status_from == "Review":
                    current_issue.add_label(current_project.repos[current_issue.repo_name].labels["rework"])
            case _:
                print("Nothing planned for going to this status: ", status_to)


def label_added(info):
    print("Label added: ", info["label"]["name"])
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
        case "0", "1", "2", "5", "8", "13", "20", "40":
            print("Points label, need to apply this in time")
            # TODO: Deal with points labels
        case _:
            print("Nothing to be done with this label: ", label_name)


if __name__ == '__main__':
    current_project = get_project_info.ProjectInfo(True)
    app.run()
