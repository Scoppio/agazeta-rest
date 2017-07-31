import time
from datetime import datetime, timedelta
from dateutil import tz


class dateTimeSummary():
    def __init__(self, day: datetime):
        self.day = day #.utcnow().date()
        self.startOfDay = datetime(self.day.year, self.day.month, self.day.day, tzinfo=tz.tzutc())
        self.endOfDay = self.startOfDay + timedelta(1)

    def __str__(self):
        return "dateTimeSummary ["+ str(self.day) + " :: " + str(self.startOfDay) + " - " + str(self.endOfDay) + "]"


def posixConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to posix time"""
    d = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    return int(time.mktime(d.timetuple()))


def datetimeConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to datetime"""
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
