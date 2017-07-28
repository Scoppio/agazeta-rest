import logging
from decouple import config
from django.test import TestCase
from arquivo.services import getValidTobTokensYield
from arquivo.models import Match, TobToken
from arquivo.documents import MMatch
from .doraR import DoraR
from settings.base import CIRCLECI

# Create your tests here.
class matchRetrieval(TestCase):
    logger = logging.getLogger('sentry.errors')
    def setUp(self):
        self.DoraR = DoraR(past_days=1, limit=True)

    def test_match_capture(self):
        '''Capture MATCH with DoraR'''
        tob_token = TobToken(username=config("TOB_INTEG_TEST_USERNAME_1"), token=config("TOB_INTEG_TEST_TOKEN_1"))
        game_data_history = self.DoraR.getTobData(tob_token=tob_token, override_limit_date=True)
        self.DoraR.matchEntryGenerator(tob_token=tob_token, game_data_history=game_data_history)
        self.logger.info("There is %d matches saved on mongodb", MMatch.objects.count())
        assert MMatch.objects.count() > 0