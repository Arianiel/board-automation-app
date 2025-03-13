import configparser
import os
from datetime import datetime
from graph_ql_interactions.github_request_functions import (
    get_content,
    open_graph_ql_query_file,
    run_query,
)

import graph_ql_interactions.card_interactions as card_i

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config_info", "config.ini"))


class BoardChecks:
    def __init__(self, cards):
        self.cards = cards
        self.release_notes = ""
        self.prs = {}
        self.problem_text = []
        self.do_the_checks()

    def do_the_checks(self):
        self.get_present_release_notes()
        self.get_release_note_prs()
        for card in self.cards:
            if card.type != "ISSUE":
                continue
            if card.repo != config["BOARD.CHECKS"]["release_notes_repo"]:
                continue
            self.verify_card_pointing_correct(card.labels, card.number, card.repo)
            self.check_if_stale(card.status, card.id, card.number)
            self.check_assignees(card.status, card.id, card.number, card.repo)
            self.check_release_notes(card)

    def update_checks(self):
        self.do_the_checks()

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
            if not list(set(labels) & set(config["BOARD.CHECKS"]["zero_points_labels"].split(","))):
                problem_text = f"ERROR: Zero-point label found for issue {number} in {repo}"
        elif points_label_count == 0:
            if not list(set(labels) & set(config["BOARD.CHECKS"]["no_points_labels"].split(","))):
                problem_text = f"ERROR: No Points labels found for issue {number} in {repo}"
        if problem_text:
            self.problem_text.append(problem_text)

    def check_assignees(self, status, ident, number, repo):
        if status not in config["BOARD.CHECKS"]["allow_unassigned"].split(","):
            if not card_i.get_assignees(ident):
                self.problem_text.append(
                    f"ERROR: Issue {number} in {repo} with {status} status does not "
                    f"have anyone assigned."
                )

    def check_if_stale(self, status, ident, number):
        # Based on self.status and intersections with the settings returned do the stale checks
        comment_errors = dict(
            item.split(":") for item in config["BOARD.CHECKS"]["comment_errors"].split(",")
        )
        label_warnings = dict(
            item.split(":") for item in config["BOARD.CHECKS"]["label_warnings"].split(",")
        )
        label_errors = dict(
            item.split(":") for item in config["BOARD.CHECKS"]["label_errors"].split(",")
        )
        if status in comment_errors.keys():
            self.check_if_last_comment_stale(comment_errors[status], ident, number, status)
        elif status in label_errors.keys() or status in label_warnings.keys():
            self.check_if_label_status_stale(label_warnings, label_errors, ident, number)

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

    def get_present_release_notes(self):
        self.release_notes = get_content(
            repo_owner=config["GITHUB.INTERACTION"]["org_name"],
            repo_name=config["BOARD.CHECKS"]["release_notes_repo"],
            file_path=config["BOARD.CHECKS"]["release_notes_file_path"],
            branch=config["BOARD.CHECKS"]["release_notes_branch"],
        )

    def get_release_note_prs(self):
        repos_query = open_graph_ql_query_file("findOpenPullRequestsInRepo.txt")
        result = run_query(
            repos_query.replace("<ORG_NAME>", config["GITHUB.INTERACTION"]["org_name"]).replace(
                "<REPO>", config["BOARD.CHECKS"]["release_notes_repo"]
            )
        )
        for value in result["data"]["repository"]["pullRequests"]["nodes"]:
            self.prs[value["title"]] = value["bodyText"]

    def check_release_notes(self, card):
        # if card.status in self.status_needing_release_notes:
        #     print(f"========={card.name}==========")
        #     print(list(set(card.labels) & set(self.release_note_exempt_labels)))
        if card.status in config["BOARD.CHECKS"]["need_notes"].split(","):
            # TODO
            print(f"******{card.name}******")
            print(list(set(card.labels) & set(config["BOARD.CHECKS"]["notes_exempt"].split(","))))
            if not list(set(card.labels) & set(config["BOARD.CHECKS"]["notes_exempt"].split(","))):
                print(f"{card.number} needs release notes")
                card_in_release_notes = False
                card_in_prs = False
                if card.name in self.release_notes:
                    card_in_release_notes = True
                    print(f"{card.name} is on main branch.")
                for pr in self.prs.keys():
                    if card.name in pr:
                        card_in_prs = True
                        print(f"{card.name} has an associated PR by title")
                    if card.name in self.prs[pr]:
                        card_in_prs = True
                        print(f"{card.name} has an associated PR by body")
                # Hard coding as this is complicated, and want to have something that works ASAP
                if card_in_release_notes and card_in_prs:
                    self.problem_text.append(
                        f"ERROR: Issue {card.number} is {card.status} and has both release notes "
                        f"and open PRs."
                    )
                    return
                if not card_in_release_notes and not card_in_prs:
                    self.problem_text.append(
                        f"ERROR: Issue {card.number} is {card.status} and has no release notes or "
                        f"PRs for release notes."
                    )
                    return
                if card.status == "Done":
                    if not card_in_release_notes and card_in_prs:
                        self.problem_text.append(
                            f"ERROR: Issue {card.number} is {card.status} and has open PRs for "
                            f"release notes."
                        )

                if card.status == "Review":
                    if card_in_release_notes and not card_in_prs:
                        self.problem_text.append(
                            f"ERROR: Issue {card.number} is {card.status} and has an entry in the "
                            f"release notes without being completed."
                        )
