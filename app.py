import asyncio
import tornado
from github_interactions import get_project_info, update_item_info
import os
import hashlib
import hmac
import configparser

# Initialise the classes that will be needed for the overall app
current_project = get_project_info.ProjectInfo()
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config_info","config.ini"))
secret = config["GITHUB.INTERACTION"]["webhook_secret"]
host = config["WWW.INTERACTION"]["host"]
port = config["WWW.INTERACTION"]["port"]


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("This probably already exists")


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(os.path.dirname(__file__), "pi_and_sprint_actions", "test_form.html"))

    def post(self):
        name = self.get_argument("name")
        self.write(f"Hello, {name}!")


class SprintHandler(tornado.web.RequestHandler):
    def get(self):
        print(current_project.current_sprint)
        self.render(os.path.join(os.path.dirname(__file__), "pi_and_sprint_actions", "sprint_data.html"),
                    current_sprint=current_project.current_sprint, next_sprint=current_project.next_sprint)

    def post(self):
        self.write(f"This will update the values for the sprint changeover")


class WebhookError(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


def verify_signature(payload_body, secret_token, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256.

    Raise and return 403 if not authorized.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not signature_header:
        raise WebhookError(status_code=403, detail="x-hub-signature-256 header is missing!")
    hash_object = hmac.new(secret_token.encode('utf-8'), msg=payload_body, digestmod=hashlib.sha256)
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise WebhookError(status_code=403, detail="Request signatures didn't match!")


class WebhookHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            verify_signature(self.request.body,secret,self.request.headers["X-Hub-Signature-256"])
        except WebhookError as e:
            print("Found a signature issue: " + e.detail)
            self.set_status(e.status_code)
            return
        request = tornado.escape.json_decode(self.request.body)
        # This is assuming a post from GitHub, other sources will not do much
        match request["action"]:
            case "unlabeled":
                print("Label removed, nothing to do: ", request["label"]["name"])
            case "labeled":
                label_added(request)
            case "edited":
                match request["changes"]["field_value"]["field_name"]:
                    case "Labels":
                        # Labels should already have been handled elsewhere
                        pass
                    case "Status":
                        status_changed(request)
                    case _:
                        print("Nothing decided yet for: " + request["changes"]["field_value"]["field_name"])
            case _:
                print("No cases for action: ", request["action"])


# Display the burndown chart of the IBEX board
class BurndownHandler(tornado.web.RequestHandler):
    def get(self):
        # Update the display before rendering
        current_project.current_burndown.update_display()
        self.render(os.path.join(os.path.dirname(__file__), "burndown_interactions/burndown-points.html"))


def status_changed(info):
    if info["projects_v2_item"]["content_type"] == "Issue":
        try:
            status_from = info["changes"]["field_value"]["from"]["name"]
        except KeyError:
            status_from = "Unknown"
        try:
            status_to = info["changes"]["field_value"]["to"]["name"]
        except KeyError:
            status_to = "Unknown"
        current_issue = update_item_info.IssueToUpdate(info["projects_v2_item"]["content_node_id"])
        current_issue.get_repo()
        current_project.add_repo(current_issue.repo_name)
        match status_from:
            case "Done":
                # Nothing to do for Done
                pass
            case "In Progress":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["in progress"])
            case "Impeded":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["impeded"])
            case "Review":
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["review"])
                current_issue.remove_label(current_project.repos[current_issue.repo_name].labels["under review"])
            case "Backlog":
                # Nothing to do for Backlog here
                pass
            case _:
                print("Nothing planned for going from this status: ", status_from)
        match status_to:
            case "Done":
                # Nothing to do for Done
                pass
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
            pass
            # print("Nothing to be done with this label: ", label_name)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestHandler),
        (r"/burndown", BurndownHandler),
        (r"/webhook", WebhookHandler),
        (r"/sprint", SprintHandler),
    ])


async def main():
    app = make_app()
    app.listen(port, host)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
