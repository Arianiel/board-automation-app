import configparser
import os
from datetime import datetime
from github_interactions.card_info import CardInfo

import graph_ql_interactions.card_interactions as card_i

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))


class BoardChecks:
    def __init__(self, cards):
        self.cards = cards
        self.cards_list = []
        for card in self.cards:
            self.cards_list.append(CardInfo(card))
        self.allowed_zero_points = []
        self.allowed_no_points = []
        self.comment_errors = {}
        self.label_warnings = {}
        self.label_errors = {}
        self.allow_unassigned = {}
        self.get_config_settings()
        self.problem_text = []
        self.do_the_checks()

    def do_the_checks(self):
        for card in self.cards_list:
            self.verify_card_pointing_correct(card.labels, card.number, card.repo)
            self.check_if_stale(card.status, card.id, card.number)
            self.check_assignees(card.status, card.id, card.number, card.repo)

    def update_checks(self):
        self.do_the_checks()

    def get_config_settings(self):
        # Get the items from the config file
        try:
            self.allowed_zero_points = config["BOARD.CHECKS"]["zero_points_labels"].split(",")
            self.allowed_no_points = config["BOARD.CHECKS"]["no_points_labels"].split(",")
        except KeyError:
            # A Key Error here will mean an absence of settings which can be ignored as appropriate
            pass

        # Get the values for the stale settings from the config file
        try:
            self.comment_errors = dict(
                item.split(": ") for item in config["STALE.SETTINGS"]["comment_errors"].split(", ")
            )
            self.label_warnings = dict(
                item.split(": ") for item in config["STALE.SETTINGS"]["label_warnings"].split(", ")
            )
            self.label_errors = dict(
                item.split(": ") for item in config["STALE.SETTINGS"]["label_errors"].split(", ")
            )
        except KeyError:
            # A Key Error here will mean no stale settings, so nothing to test
            pass

        # Get the list of labels which indicate tickets can be unassigned
        try:
            self.allow_unassigned = config["BOARD.RULES"]["allow_unassigned"].split(", ")
        except KeyError:
            pass

    def verify_card_pointing_correct(self, labels, number, repo):
        points_label_count = 0
        zero_point_label = False
        problem_text = None
        for label in labels:
            if label.isdigit():
                points_label_count += 1
            if label == "0":
                zero_point_label = True
        if points_label_count > 1:
            problem_text = f"ERROR: Multiple Points labels found for issue {number} in {repo}"
        elif zero_point_label:
            if not list(set(labels) & set(self.allowed_zero_points)):
                problem_text = f"ERROR: Zero-point label found for issue {number} in {repo}"
        elif points_label_count == 0:
            if not list(set(labels) & set(self.allowed_no_points)):
                problem_text = f"ERROR: No Points labels found for issue {number} in {repo}"
        if problem_text:
            self.problem_text.append(problem_text)

    def check_assignees(self, status, ident, number, repo):
        if status not in self.allow_unassigned:
            if not card_i.get_assignees(ident):
                self.problem_text.append(
                    f"ERROR: Issue {number} in {repo} with {status} status does not "
                    f"have anyone assigned."
                )

    def check_if_stale(self, status, ident, number):
        # Based on self.status and intersections with the settings returned do the stale checks
        if status in self.comment_errors.keys():
            self.check_if_last_comment_stale(self.comment_errors[status], ident, number, status)
        elif status in self.label_errors.keys() or status in self.label_warnings.keys():
            self.check_if_label_status_stale(self.label_warnings, self.label_errors, ident, number)

    def check_if_last_comment_stale(self, duration, ident, number, status):
        last_comment = datetime.strptime(
            card_i.get_when_last_commented_created_on_issue(ident), "%Y-%m-%dT%H:%M:%SZ"
        )
        today_to_compare = datetime.today()
        if (today_to_compare - last_comment).days >= int(duration):
            self.problem_text.append(
                f"ERROR: Issue {number} in {status} last had a comment added 28 days or more ago."
            )

    def check_if_label_status_stale(self, warning_list, error_list, ident, number):
        labels = card_i.get_when_labels_were_added_to_issue(ident)
        today_for_labels = datetime.today()
        for label in labels:
            label_in_place_since = (
                today_for_labels - datetime.strptime(labels[label], "%Y-%m-%dT%H:%M:%SZ")
            ).days
            if label in error_list:
                if label_in_place_since >= int(error_list[label]):
                    self.problem_text.append(
                        f"ERROR: Issue {number} had {label} label added more than "
                        f"{int(error_list[label])} days ago."
                    )
                    return
                if label_in_place_since >= int(warning_list[label]):
                    self.problem_text.append(
                        f"WARNING: Issue {number} had {label} label added"
                        f" more than {int(warning_list[label])} days ago."
                    )
                    return
