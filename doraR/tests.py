import logging
from decouple import config
from django.test import TestCase
from arquivo.services import tobTokenServices, matchServices
from arquivo.documents import MMatch
from .doraR import DoraR

class matchRetrieval(TestCase):

    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        self.DoraR = DoraR(past_days=1, limit=True, override_limit_date=True)


    def test_match_capture(self):
        '''Capture MATCH with DoraR and persist it'''
        tob_token = tobTokenServices.createTobToken(username=config("TOB_INTEG_TEST_USERNAME_1"), token=config("TOB_INTEG_TEST_TOKEN_1"), server="a")
        game_data_history = self.DoraR.getTobData(tob_token=tob_token)
        self.DoraR.matchEntryGenerator(tob_token=tob_token, game_data_history=game_data_history)

        self.logger.debug("There is %d matches saved on mongodb", MMatch.objects.count())

        self.logger.debug("%s, %s",str(MMatch.objects.first()), MMatch.objects.first().__repr__())

        assert len(game_data_history) > 0
        assert game_data_history[0]["id"] != None
        assert len(matchServices.getAllMatches()) > 0
