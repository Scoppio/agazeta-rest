# This service captures the data using Dora R. as base
# coding: utf-8
import os
import json
import time
import logging
import requests
from datetime import datetime
from .dao import userDAO
from .models import TobToken
from .documents import MMatch, MCardPlayed
from django.db.utils import IntegrityError
from settings.base import MINNING_URLS

logger = logging.getLogger('sentry.errors')


def createTobToken(username, token, server, is_active=True):
    tobToken = TobToken(username=username, token=token, server=server, is_active=is_active)
    try:
        tobToken.save()
        logger.info("Created TobToken for username %s", username)
    except Exception as e:
        logger.info("TobToken for username %s failed to be saved", username)
        raise IntegrityError("TobToken for username " + username + " failed to be saved")


def createTobTokenAndInviteUserToRegister(server, email, username, token, subed, valid):
    # tobToken = createTobToken(server=server, email=email, token=token, username=username, subed=subed)
    # _email = "" if type(email) != str else email
    # TODO: Add invitation system to this system
    # logger.info("Created User % for email %s", _email)
    raise NotImplementedError


def verifyTobToken(username=None, token=None, tobToken=None):
    if tobToken:
        username=tobToken.username
        token=tobToken.token

    url = MINNING_URLS["Track-o-Bot"]
    try:
        response = requests.get(url, data={'page': 1, 'username': username, 'token': token})
    except Exception as e:
        logger.error("Failed to capture data from {}".format(url))

    try:
        assert response.status_code == 200

        data = json.loads(response.text)
        if len(data['meta'].keys()):
            logger.info("Token %s is valid", username)
            return True
        else:
            logger.info("Token %s is invalid", username)
            return False

    except AssertionError as e:
        if response.status_code == 401:
            logger.info("The token %s is invalid", username)
            return False
        else:
            logger.error("The url responded with code %d", response.status_code)
            return None
    except Exception as e:
        logger.error("An unexpected error occurred when trying to read the json from %s", username)
        return None


def addTokenToUser(tobToken, user):
    tobToken.user=user
    tobToken.save()


def getValidTobTokensYield(limit : int=0):
    """Get username, token and account from database"""
    sqlret = TobToken.objects.filter(is_active=True) if not limit \
        else TobToken.objects.filter(is_active=True)[:limit]

    logger.debug("{} tob tokens retrieved from database".format(len(sqlret)))

    for i, row in enumerate(sqlret):
        logger.debug("tob token {} of {} - username {} - account {}".format(i, len(sqlret), row.username, row.user))
        yield row


def getAllTobTokensYield(limit : int=0):
    """Get username, token and account from database"""
    sqlret = TobToken.objects.all() if not limit \
        else TobToken.objects.all()[:limit]

    logger.debug("{} tob tokens retrieved from database".format(len(sqlret)))

    for i, row in enumerate(sqlret):
        logger.debug("tob token {} of {} - username {} - account {}".format(i, len(sqlret), row.username, row.user))
        yield row


def posixConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to posix time"""
    d = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    return int(time.mktime(d.timetuple()))


def datetimeConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to datetime"""
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')


def saveMatchOnMongo(match_id, match_mode, user, date, blue_rank, blue_hero, blue_deck, red_hero, red_deck, turns_played,
               red_starts, blue_won, cards):

    # First check if the match exists
    try:
        match = MMatch.objects.get(match_id=match_id)
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
            blueCards.append(MCardPlayed(card=str(card['card']['id']),
                                   turn_played = card['turn'], is_spawned=False))
        else:
            redCards.append(MCardPlayed(card=str(card['card']['id']),
                                   turn_played=card['turn'], is_spawned=False))

    match = MMatch(
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

    return