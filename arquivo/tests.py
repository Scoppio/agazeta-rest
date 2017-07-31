import logging
import datetime
from dateutil import tz
from decouple import config
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from model_mommy import mommy
from arquivo.dao import userDAO, matchDAO
from arquivo.documents import MMatch, MCardPlayed
from arquivo.models import Profile, TobToken
from arquivo.services import tobTokenServices
from arquivo.utils import dateUtils
class UserAndProfileCreation(TestCase):

    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        self.user = mommy.make('User')
        self.userSaved = User(username="Test_user", password="154$a%pla9vb")
        self.profile = Profile(user=self.userSaved, account_type=Profile.ACCOUNT_TYPE[0], partner_sub=True,
                               newsletter_sub=False)

    def test_saving_user_profile(self):
        '''Saving user should also save its profile'''
        self.userSaved.save()
        assert len(User.objects.filter(username="Test_user")) == 1
        assert self.userSaved.profile.partner_sub == True

    def test_user_creation(self):
        '''Create USER with a related PROFILE'''
        assert self.user.profile != None
        assert self.user.profile.avatar != None

    def test_creation_of_profile_for_user(self):
        '''Use createProfileForUser to create profile'''
        userDAO.createProfileForUser(self.userSaved, Profile.ACCOUNT_TYPE[0], True, True)
        assert self.userSaved.profile.account_type == Profile.ACCOUNT_TYPE[0]


class ServiceTests(TestCase):

    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        tobTokenServices.createTobToken("username_1", "token_1", 'a', is_active=True)
        tobTokenServices.createTobToken("username_2", "token_2", 'a', is_active=False)

    def test_getAllTokensYeld(self):
        '''Verify if token grabber functions actually work'''
        token_found = 0
        for _ in tobTokenServices.getValidTobTokensYield():
           token_found += 1

        self.logger.info("Were found %d valid tokens", token_found)

        assert token_found == 1

        token_found = 0
        for _ in tobTokenServices.getAllTobTokensYield():
           token_found += 1

        self.logger.info("Were found %d tokens in total", token_found)
        assert token_found == 2

    def test_token_creation_exception(self):
        '''Check that it is not possible to create duplicated tokens'''
        self.assertRaises(IntegrityError, tobTokenServices.createTobToken, "username_2", "token_2", 'a', False)

    def test_token_validity(self):
        '''Check if the token is valid or invalid, returns None when it is invalid'''
        assert tobTokenServices.verifyTobToken(username="username_2", token="token_2") == False
        assert tobTokenServices.verifyTobToken(username=config("TOB_INTEG_TEST_USERNAME_1"), token=config("TOB_INTEG_TEST_TOKEN_1")) == True

        for tobToken in tobTokenServices.getAllTobTokensYield(1):
            assert tobTokenServices.verifyTobToken(tobToken=tobToken) == False

    def test_user_creation_with_tob_token(self):
        '''Declare a tobToken to be of a particular user'''
        for tobToken in tobTokenServices.getAllTobTokensYield(1):

            user = userDAO.createUser(username="TestUser", password="897a8sda9", first_name="name", last_name="00a", email="a@a.a")

            tobTokenServices.addTokenToUser(tobToken, user)

            assert tobToken.user == user

    def test_date_conversions(self):
        '''Test if the human-readable timestamp to datetime/posix converters actually work'''
        day = dateUtils.dateTimeSummary(datetime.datetime(2016, 12, 2, 2, 29, 9))
        print(day)
        assert dateUtils.datetimeConversion(date='2016-12-02T02:29:09.000Z') == datetime.datetime(2016, 12, 2, 2, 29, 9)
        assert dateUtils.posixConversion(date='2016-12-02T02:29:09.000Z') == 1480652949
        assert day.startOfDay == datetime.datetime(2016, 12, 2, 0, 0, 0, tzinfo=tz.tzutc())
        assert day.endOfDay == datetime.datetime(2016, 12, 3, 0, 0, 0, tzinfo=tz.tzutc())


class MongoDbDocuments(TestCase):

    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        card1 = matchDAO.card(card="HAL-001", turn_played=1, is_spawned=False)
        card2 = matchDAO.card(card="TES-055", turn_played=2, is_spawned=False)
        card3 = matchDAO.card(card="BOL-124", turn_played=3, is_spawned=False)
        card4 = matchDAO.card(card="JUN-998", turn_played=4, is_spawned=False)

        self.match = matchDAO.match(match_id=2, match_mode="test", user=[42,99], date=datetime.datetime.now(),
                            blue_rank=20, blue_hero="Rogue", blue_deck="Random Blue Deck",
                            red_deck="Random Red Deck", red_hero="Warrior", turns_played=99, red_starts=False,
                            blue_won=True, blue_played_cards=[card1,card2], red_played_cards=[card4,card3])

    def test_Mongo_Match_Created(self):
        '''Check if the match has the important data inside related to cards and users'''
        assert len(self.match.blue_played_cards) == 2
        assert len(self.match.user) == 2