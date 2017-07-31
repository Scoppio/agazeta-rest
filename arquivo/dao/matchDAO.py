import json
import logging
from mongoengine import Q
from functools import reduce
from django.db.utils import IntegrityError
from arquivo.documents import MMatch, MCardPlayed
from arquivo.utils.dateUtils import dateTimeSummary

logger = logging.getLogger('sentry.errors')


def findAll():
    return [match for match in MMatch.objects.all()]


def findOne(match_id: int):
    return MMatch.objects.get(match_id=match_id)


def findOneByObjId(id: int):
    return MMatch.objects.get(id=id)


def findAllOnDate(date):
    day = dateTimeSummary(date)

    query = [
        {'date__gte' : day.startOfDay},
        {'date__lte' : day.endOfDay}
    ]

    return [match for match in MMatch.objects.find({'$and' : query})]


def findGamesByCardPlayed(card):

    query = [
        {"blue_cards_played": card},
        {"red_cards_played": card}
    ]

    return [match for match in MMatch.objects.find({'$or' : query})]


def match(match_id, match_mode, date, blue_rank, blue_hero, blue_deck, red_hero,
           red_deck, turns_played, red_starts, blue_won, blue_played_cards, red_played_cards, user=[]):

    return MMatch(
        match_id=match_id,
        match_mode=match_mode,
        date=date,
        user=user,
        blue_rank=blue_rank,
        blue_hero=blue_hero,
        blue_deck=blue_deck,
        red_hero=red_hero,
        red_deck=red_deck,
        turns_played=turns_played,
        red_starts=red_starts,
        blue_won=blue_won,
        blue_played_cards=blue_played_cards,
        red_played_cards=red_played_cards
    )


def card(card, turn_played, is_spawned, save=False):
    newCard = MCardPlayed(card=card, turn_played=turn_played, is_spawned=is_spawned)
    if save:
        newCard.save()
    return newCard


def findGamesGivenQuery(query_input):

    def prepare_condition(condition):
        field = [condition['field'], condition['operator']]
        field = (s for s in field if s)
        field = '__'.join(field)
        return {field: condition['value']}

    def prepare_conditions(row):
        return (Q(**prepare_condition(condition)) for condition in row)

    def join_conditions(row):
        return reduce(lambda a, b: a | b, prepare_conditions(row))

    def join_rows(rows):
        return reduce(lambda a, b: a & b, rows)

    # query_input = [
    #     [
    #         {
    #             "field": "some_field",
    #             "operator": "gt",
    #             "value": 30
    #         },
    #         {
    #             "field": "some_field",
    #             "operator": "lt",
    #             "value": 40
    #         },
    #         {
    #             "field": "some_field",
    #             "operator": "",
    #             "value": 35
    #         }
    #     ],
    #     [
    #         {
    #             "field": "another_field",
    #             "operator": "istartswith",
    #             "value": "test"
    #         }
    #     ]
    # ]

    query = join_rows(join_conditions(row) for row in query_input)

    print(json.dumps(query.to_query(None), indent=4))
    # {
    #     "$and": [
    #         {
    #             "$or": [
    #                 {
    #                     "some_field": {
    #                         "$gt": 30
    #                     }
    #                 },
    #                 {
    #                     "some_field": {
    #                         "$lt": 40
    #                     }
    #                 },
    #                 {
    #                     "some_field": 35
    #                 }
    #             ]
    #         },
    #         {
    #             "another_field": "test"
    #         }
    #     ]
    # }



