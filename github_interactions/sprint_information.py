import datetime


class SprintInfo:
    def __init__(self, values):
        if "Next" in values["name"]:
            self.sprint_name = values["name"][9:-1]
        else:
            self.sprint_name = values["name"]
        self.sprint_year = self.sprint_name[:4]
        self.sprint_month = self.sprint_name[5:7]
        self.sprint_day = self.sprint_name[8:]
        self.sprint_id = values["id"]
        self.sprint_start_date = datetime.datetime(year=int(self.sprint_year), month=int(self.sprint_month),
                                                   day=int(self.sprint_day))

    def __str__(self):
        return str(self.sprint_start_date)