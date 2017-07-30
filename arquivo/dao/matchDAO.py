import logging
from django.db.utils import IntegrityError
from arquivo.documents import MMatch
from arquivo.utils.dateUtils import dateTimeSummary

logger = logging.getLogger('sentry.errors')


def findAll():
    return [match for match in  MMatch.objects]


def findOne(id : int):
    return MMatch.objects(id=id)[0]


def findAllOnDate(date):
    day = dateTimeSummary(date)
    return [match for match in MMatch.objects(date__lte=day.endOfDay, date__gte=day.startOfDay)]
