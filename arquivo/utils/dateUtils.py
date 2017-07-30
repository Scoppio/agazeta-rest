import datetime
from datetime import timedelta
from dateutil import tz

class dateTimeSummary():
    def __init__(self, day : datetime):
        self.today = day.utcnow().date()
        self.startOfDay = datetime(self.today.year, self.today.month, self.today.day, tzinfo=tz.tzutc())
        self.endOfDay = self.start + timedelta(1)