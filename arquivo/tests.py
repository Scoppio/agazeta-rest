import logging
import datetime
import random
from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from .models import Match, TobToken, CardPlayed
from .documents import MMatch, MCardPlayed

class MatchRelationshipTestCase(TestCase):
    def setUp(self):
        self.match = mommy.make('arquivo.Match')
        self.blueCards = mommy.make('arquivo.CardPlayed', _quantity=12, match=self.match)
        self.redCards = mommy.make('arquivo.CardPlayed', _quantity=10, match=self.match)
        [self.match.red_played_cards.add(redCard) for redCard in self.redCards]
        [self.match.blue_played_cards.add(blueCard) for blueCard in self.blueCards]

    def test_match_relationship(self):
        '''MATCH and CARDS relationship'''
        assert len(self.match.blue_played_cards.all()) == 12
        assert len(self.match.red_played_cards.all()) == 10
        self.assertEqual(self.blueCards[0].match, self.match)
        self.assertEqual(self.redCards[0].match, self.match)

    def test_user_creation(self):
        '''Create USER with a related PROFILE'''
        user = mommy.make('User')
        assert user.profile != None
        assert user.profile.avatar != None

class MongoDbDocuments(TestCase):
    logger = logging.getLogger('sentry.errors')

    def setUp(self):
        card1 = MCardPlayed(card="HAL-001", turn_played=1, is_spawned=False).save()
        card2 = MCardPlayed(card="TES-055", turn_played=2, is_spawned=False).save()
        card3 = MCardPlayed(card="BOL-124", turn_played=3, is_spawned=False).save()
        card4 = MCardPlayed(card="JUN-998", turn_played=4, is_spawned=False).save()
        try:
            MMatch(match_id=1, match_mode="test", user=[42,99], date=datetime.datetime.now(),
                                 blue_rank=20, blue_hero="Rogue", blue_deck="Random Blue Deck",
                                 red_deck="Random Red Deck", red_hero="Warrior", turns_played=99, red_starts=False,
                                 blue_won=True, blue_played_cards=[card1,card2], red_played_cards=[card4,card3]).save()
        except Exception as e:
            pass

    def test_Mongo_Match_Created(self):
        self.logger.info("Number of documents MMatch = %d", MMatch.objects.count())
        assert MMatch.objects.count() != 0
        assert len(MMatch.objects.get(match_id=1).blue_played_cards) == 2
        assert len(MMatch.objects.get(match_id=1).user) == 2

    def doCleanups(self):
        MMatch.objects.get(match_id=1).delete()
        self.logger.info("Number of documents MMatch = %d", MMatch.objects.count())