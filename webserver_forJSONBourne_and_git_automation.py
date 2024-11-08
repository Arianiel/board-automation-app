from builtins import str
import json
import logging
import os
from logging.handlers import TimedRotatingFileHandler
import tornado.ioloop
import tornado.web
import asyncio
import hashlib
import hmac
import configparser
import plotly.graph_objects as go

from external_webpage.request_handler_utils import get_detailed_state_of_specific_instrument, \
    get_summary_details_of_all_instruments, get_instrument_and_callback
from external_webpage.web_scrapper_manager import WebScrapperManager
from external_webpage.instrument_scapper import scraped_data, scraped_data_lock

# Additions for github automation
from github_interactions import automation_information, update_item_info

# Set up JSON_bourne logger
logger = logging.getLogger('JSON_bourne')
log_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log', 'JSON_bourne.log')
handler = TimedRotatingFileHandler(log_filepath, when='midnight', backupCount=30)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Set up project management logger
pm_log_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'log', 'board_automation.log')
pm_logger = logging.getLogger('board_automation')
pm_handler = TimedRotatingFileHandler(pm_log_filepath, when='midnight', backupCount=30)
pm_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
pm_logger.setLevel(logging.INFO)
pm_logger.addHandler(pm_handler)


def pm_logging(message, message_level):
    if app_log_level == "developer":
        print(message)
    match message_level:
        case "error":
            pm_logger.exception(message)
        case "info":
            if app_log_level in ["developer", "info", "all"]:
                pm_logger.info(message)
        case "debug":
            if app_log_level in ["developer", "debug", "all"]:
                pm_logger.debug(message)

# use dataweb2.isis.rl.ac.uk / ndaextweb3-data.nd.rl.ac.uk (130.246.92.89)
# HOST, PORT = '130.246.92.89', 443


# Initialise the classes that will be needed for the overall automation work
current_project = get_project_info.AutomationInfo()
# Get the items from the config file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config_info", "config.ini"))
try:
    secret = config["GITHUB.INTERACTION"]["webhook_secret"]
    host = config["WWW.INTERACTION"]["host"]
    port = config["WWW.INTERACTION"]["port"]
    app_log_level = config["SETTINGS"]["log_level"]
except KeyError as ke:
    match ke.args[0]:
        case "GITHUB.INTERACTION", "WWW.INTERACTION":
            pm_logging("Config section needed but not present: {}".format(ke), "error")
        case "log_level":
            app_log_level = ""
        case _:
            pm_logging("Section missing from config: {}".format(ke), "error")

class MyHandler(tornado.web.RequestHandler):
    """
    Handle for web calls for Json Borne
    """

    def get(self):
        """
        This is called by BaseHTTPRequestHandler every time a client does a GET.
        The response is written to self.wfile
        """
        path = self.request.uri
        instrument = "Not set"
        try:
            instrument, callback = get_instrument_and_callback(path)

            # Debug is only needed when debugging
            logger.debug("Connection from {} looking at {}".format(self.request.remote_ip, instrument))

            with scraped_data_lock:
                if instrument == "ALL":
                    ans = {
                        "error": web_manager.instrument_list_retrieval_errors(),
                        "instruments": get_summary_details_of_all_instruments(scraped_data)}

                else:
                    ans = get_detailed_state_of_specific_instrument(instrument, scraped_data)

            try:
                ans_as_json = str(json.dumps(ans))
            except Exception as err:
                raise ValueError("Unable to convert answer data to JSON: {}".format(err))

            response = "{}({})".format(callback, ans_as_json)

            self.set_status(200)
            self.set_header('Content-type', 'text/html')
            self.write(response.encode("utf-8"))
        except ValueError as e:
            logger.exception("Value Error when getting data from {} for {}: {}".format(
                self.request.remote_ip, instrument, e))
            self.set_status(400)
        except Exception as e:
            logger.exception("Exception when getting data from {} for {}: {}".format(
                self.request.remote_ip, instrument, e))
            self.set_status(404)

    def log_message(self, format, *args):
        """ By overriding this method and doing nothing we disable writing to console
         for every client request. Remove this to re-enable """
        return

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

# Handlers anf functions for automation
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
        # Update the display before displaying
        current_project.current_burndown.update_display()
        self.write(current_project.current_burndown.burndown_display())


class SprintHandler(tornado.web.RequestHandler):
    def get(self):
        print(current_project.current_sprint)
        self.render(os.path.join(os.path.dirname(__file__), "pi_and_sprint_actions", "sprint_data.html"),
                    current_sprint=current_project.current_sprint, next_sprint=current_project.next_sprint)

    def post(self):
        current_project.update_sprints()
        self.render(os.path.join(os.path.dirname(__file__), "pi_and_sprint_actions", "updated_sprint_data.html"),
                    current_sprint=current_project.current_sprint, next_sprint=current_project.next_sprint)


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
        case _:
            pass
            # print("Nothing to be done with this label: ", label_name)


if __name__ == '__main__':
    # It can sometime be useful to define a local instrument list to add/override the instrument list do this here
    # E.g. to add local instrument local_inst_list = {"LOCALHOST": ("localhost", "MYPVPREFIX")}
    local_inst_list = {}
    web_manager = WebScrapperManager(local_inst_list=local_inst_list)
    web_manager.start()

    # As documented at https://github.com/tornadoweb/tornado/issues/2608
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        application = tornado.web.Application([
            (r"/", MyHandler),
            (r"/burndown", BurndownHandler),
            (r"/webhook", WebhookHandler),
            (r"/sprint", SprintHandler),
        ])
        http_server = tornado.httpserver.HTTPServer(application, ssl_options={
            "certfile": r"C:\Users\ibexbuilder\dataweb2_isis_rl_ac_uk.crt",
            "keyfile": r"C:\Users\ibexbuilder\dataweb2_isis_rl_ac_uk.key",
        })
        http_server.listen(port, host)
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("Shutting down")
        web_manager.stop()
        web_manager.join()
