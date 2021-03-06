import uuid
from mongoengine import *
from settings.base import MONGODBNAME, MONGODBURL, MONGODBPORT


connect(MONGODBNAME, host=MONGODBURL, port=MONGODBPORT)


class MCardPlayed(Document):
    card = StringField(max_length=20, required=True)
    turn_played = IntField(required=True)
    is_spawned = BooleanField(default=False)

    def __str__(self):
        return "card_played [card={} turn_played={} is_spawned={}]".format(self.card, self.turn_played, self.is_spawned)

    def __dict__(self):
        return {"card": self.card, "turn_played": self.turn_played, "is_spawned": self.is_spawned}

    def __repr__(self):
        return "card_played [card={}turn_played={} is_spawned={}]".format(self.card, self.turn_played, self.is_spawned)


class MMatch(Document):
    match_id = IntField(required=True, unique=True)
    match_mode = StringField(max_length=20, required=True)
    user = ListField(IntField())
    date = DateTimeField(required=True)
    blue_rank = IntField()
    blue_hero = StringField(max_length=30, required=True)
    blue_deck = StringField(max_length=30)
    red_hero = StringField(max_length=30, required=True)
    red_deck = StringField(max_length=30)
    turns_played = IntField(required=True)
    red_starts = BooleanField(required=True)
    blue_won = BooleanField(required=True)
    blue_played_cards = ListField(ReferenceField(MCardPlayed))
    red_played_cards = ListField(ReferenceField(MCardPlayed))

    meta = {
        'shard_key': ('machine', 'date',)
    }

    def __str__(self):
        return "match [matchid={} date={} blue={} red={}]".format(
            self.match_id, self.date, self.blue_hero, self.red_hero)

    def __repr__(self):
        return "match [id={} matchid={} date={} blue={} red={}]".format(
            self.id, self.match_id, self.date, self.blue_hero, self.red_hero)