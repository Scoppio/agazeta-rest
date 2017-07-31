# coding: utf-8
import os
import json
import time
import logging
from datetime import datetime
from arquivo.dao import matchDAO


logger = logging.getLogger('sentry.errors')


def getAllMatches():
    return matchDAO.findAll()


def saveMatch(match_id, match_mode, user, date, blue_rank, blue_hero,
              blue_deck, red_hero, red_deck, turns_played, red_starts, blue_won, cards):

    # First check if the match exists
    try:
        match = matchDAO.findOne(match_id)
        if user.id in match.user:
            return
        else:
            match.user.add(user.id)
            logger.info("Match %d already present, user %s added to it", match.match_id, user.id)
            return

    except Exception as e:
        pass

    # if the match is here, add the user to it if he is not null
    # add the cards to it related to the match
    blueCards = []
    redCards = []
    for card in cards:
        if card['player'] == 'me':
            blueCards.append(matchDAO.card(card=str(card['card']['id']),
                                   turn_played = card['turn'], is_spawned=False))
        else:
            redCards.append(matchDAO.card(card=str(card['card']['id']),
                                   turn_played=card['turn'], is_spawned=False))

    match = matchDAO.match(
        match_id = match_id ,
        match_mode = match_mode,
        date = date,
        blue_rank = blue_rank,
        blue_hero = blue_hero,
        blue_deck = blue_deck,
        red_hero = red_hero,
        red_deck = red_deck  ,
        turns_played = turns_played,
        red_starts = red_starts,
        blue_won = blue_won,
        blue_played_cards=blueCards,
        red_played_cards=redCards
    )

    if user:
        match.user.add(user)

    try:
        match.save()
        logger.info("New match entry saved, match_id=%d", match_id)
    except Exception as e:
        logger.warning("New match entry could NOT be saved, match_id=%d, %s",match_id, e)

    if user and user.id not in match.user:
        match.user.add(user.id)
        match.save()