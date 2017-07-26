from django.test import TestCase
from django.contrib.auth.models import User
from model_mommy import mommy
from .models import Match, TobToken, CardPlayed

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