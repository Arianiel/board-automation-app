from unittest import TestCase
from unittest.mock import mock_open, patch

from burndown_interactions.burndown import Burndown


class TestBurndown(TestCase):
    def test_burndown_display(self):
        # TODO
        # Figure out how to test this!
        pass

    def test_update_display(self):
        # TODO
        # Figure out how to test this!
        pass

    def test_add_new_csv_line(self):
        # TODO
        # Figure out how to test this!
        pass

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
