import configparser
import os


class CardInfo:
    def __init__(self, card: {}):
        self.node_id = card["id"]
        self.type = card["type"]
        try:
            self.id = card["content"]["id"]
        except KeyError:
            self.id = None
        self.labels = []
        match self.type:
            case "DRAFT_ISSUE":
                self.number = card["content"]["title"]
                self.repo = "draft"
            case "ISSUE":
                self.number = card["content"]["number"]
                self.repo = card["content"]["repository"]["name"]
                try:
                    for label in card["content"]["labels"]["nodes"]:
                        self.labels.append(label["name"])
                except KeyError:
                    # Section is empty ignore it
                    pass
            case "PULL_REQUEST":
                # These are not handled yet
                self.number = None
                self.repo = None
            case _:
                self.number = None
                self.repo = None
        self.name = str(self.number)
        field_values = card["fieldValues"]["nodes"]
        self.status = None
        self.sprint = None
        self.points = 0
        for value in field_values:
            try:
                match value["field"]["name"]:
                    case "Sprint":
                        self.sprint = value["name"]
                    case "Status":
                        self.status = value["name"]
                    case "Points":
                        self.points = value["number"]
                    case "Planning Priority":
                        self.priority = value["name"]
                    case _:
                        pass
            except KeyError:
                pass
        self.allowed_zero_points = []
        self.allowed_no_points = []
        self.get_label_permissions()
        self.problem_identified = False
        self.problem_text = ""
        points_label_count = 0
        zero_point_label = False
        for label in self.labels:
            if label.isdigit():
                points_label_count += 1
            if label == '0':
                zero_point_label = True
        if points_label_count > 1:
            self.problem_identified = True
            self.problem_text = f"Multiple Points labels found for issue {self.number} in {self.repo}"
        elif zero_point_label:
            if not list(set(self.labels) & set(self.allowed_zero_points)):
                self.problem_identified = True
                self.problem_text = f"Zero-point label found for issue {self.number} in {self.repo}"
        elif points_label_count == 0:
            if not list(set(self.labels) & set(self.allowed_no_points)):
                self.problem_identified = True
                self.problem_text = f"No Points labels found for issue {self.number} in {self.repo}"


    def __str__(self):
        return self.name

    def get_label_permissions(self):
        # Get the items from the config file
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))
        try:
            self.allowed_zero_points = config["BOARD.CHECKS"]["zero_points_labels"].split(",")
            self.allowed_no_points = config["BOARD.CHECKS"]["no_points_labels"].split(",")
        except KeyError as ke:
            # A Key Error here will mean an absence of labels which can be ignored as appropriate
            pass