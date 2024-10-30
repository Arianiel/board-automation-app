#from github_interactions import get_project_info
import configparser
import os

# project = get_project_info.ProjectInfo()
# print("Project Created")
# print(project.project_number)
# print(project.sprint_ids)
# print(project.current_sprint)
# print(project.next_sprint)
# print("Updating with a lied about date")
# project.update_sprints()
# print(project.current_sprint)
# print(project.next_sprint)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))
try:
    secret = config["GITHUB.INTERACTION"]["webhook_secret"]
    host = config["WWW.INTERACTION"]["host"]
    port = config["WWW.INTERACTION"]["port"]
    app_log_level = config["SETTINGS"]["log_level"]
except KeyError as ke:
    for arg in ke.args:
        print(arg)
    match ke.args[0]:
        case "GITHUB.INTERACTION", "WWW.INTERACTION":
            print("Config section needed but not present: {}".format(ke))
        case "log_level":
            print("This would be the default log level")
        case _:
            print("Section missing from config: {}".format(ke))
