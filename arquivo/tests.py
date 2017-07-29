import logging
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from .services import getAllTobTokensYield, getValidTobTokensYield, posixConversion, datetimeConversion
from .documents import MMatch, MCardPlayed
from .models import Profile

class UserAndProfileCreation(TestCase):
    def setUp(self):
        self.user = mommy.make('User')
        self.userSaved =  User(username="Test_user", password="154$a%pla9vb")
        self.profile = Profile(user=self.userSaved, account_type=Profile.ACCOUNT_TYPE[0], partner_sub=True, newsletter_sub=False)

    def test_saving_user_profile(self):
        self.userSaved.save()
        assert len(User.objects.filter(username="Test_user")) == 1
        assert self.userSaved.profile.partner_sub == True

    def test_user_creation(self):
        '''Create USER with a related PROFILE'''
        assert self.user.profile != None
        assert self.user.profile.avatar != None

class ServiceTests(TestCase):
    def test_getAllTokensYeld(self):
        for _ in getAllTobTokensYield(1):
           assert True == False

        assert True == True

class MongoDbDocuments(TestCase):
    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        card1 = MCardPlayed(card="HAL-001", turn_played=1, is_spawned=False)
        card2 = MCardPlayed(card="TES-055", turn_played=2, is_spawned=False)
        card3 = MCardPlayed(card="BOL-124", turn_played=3, is_spawned=False)
        card4 = MCardPlayed(card="JUN-998", turn_played=4, is_spawned=False)

        self.match = MMatch(match_id=2, match_mode="test", user=[42,99], date=datetime.datetime.now(),
                            blue_rank=20, blue_hero="Rogue", blue_deck="Random Blue Deck",
                            red_deck="Random Red Deck", red_hero="Warrior", turns_played=99, red_starts=False,
                            blue_won=True, blue_played_cards=[card1,card2], red_played_cards=[card4,card3])

    def test_Mongo_Match_Created(self):
        assert len(self.match.blue_played_cards) == 2
        assert len(self.match.user) == 2