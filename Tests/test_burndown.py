from unittest import TestCase
from unittest.mock import mock_open, patch

import requests_mock
from datetime import datetime
from collections import Counter

from Tests.test_helpers import snapshot_name_to_status_lookup, build_response, QlCommand
from burndown_interactions.burndown import Burndown


class TestBurndown(TestCase):
    # Not writing the test below as this is a figure generation inbuilt to an imported library
    # def test_burndown_display(self):
        
    def test_update_display(self):
        # TODO
        # Figure out how to test this!
        pass

    @requests_mock.mock()
    def test_add_new_csv_line(self, m):
        expected_snapshot = {
            "ready": {"count": 3, "points": 3},
            "rework": {"count": 1, "points": 1},
            "in_progress": {"count": 2, "points": 2},
            "impeded": {"count": 1, "points": 1},
            "review": {"count": 3, "points": 3},
            "done": {"count": 4, "points": 4},
        }
        alternative = [datetime.today().strftime("%Y-%m-%d")]
        for entry in expected_snapshot:
            if entry == "rework":
                continue
            alternative.append(",")
            alternative.append(str(expected_snapshot[entry]["count"]))
        alternative.append("\n")
        sprint_name = "sprint"
        m.post('https://api.github.com/graphql', text=build_response(QlCommand.findCardInfo, card_type="points_snapshot",
                                        expected_snapshot=expected_snapshot, sprint_name=sprint_name))
        test_class = Burndown(org_name="", project_number="", current_sprint_name=sprint_name, next_sprint_name="", sprints={})
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=True):
            test_class.add_new_csv_line()
        open_mock.assert_called_with(test_class.burndown_csv, "a")
        open_mock.return_value.write.assert_called_once_with("".join(alternative))

    def test_fill_csv_lines(self):
        # TODO
        # Figure out how to test this!
        pass

    def test_add_csv_titles(self):
        test_class = Burndown(org_name="", project_number="", current_sprint_name="", next_sprint_name="", sprints={})
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=True):
            test_class.add_csv_titles()
        open_mock.assert_called_with(test_class.burndown_csv, "w")
        open_mock.return_value.write.assert_called_once_with(test_class.csv_headings)

    def test_get_data_frame(self):
        # TODO
        # Figure out how to test this!
        pass

    def test_change_sprint(self):
        test_class = Burndown(org_name="", project_number="", current_sprint_name="", next_sprint_name="", sprints={})
        open_mock = mock_open()
        with patch("builtins.open", open_mock, create=True):
            test_class.change_sprint()
        open_mock.assert_called_with(test_class.burndown_csv, "w")
        open_mock.return_value.write.assert_called_once_with(test_class.csv_headings)
