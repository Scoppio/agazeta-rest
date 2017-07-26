# This service captures the data using Dora R. as base
# coding: utf-8
import os
import json
import time
import logging
import requests
import pandas as pd
from datetime import datetime
from .models import TobToken, Match, CardPlayed
from django.contrib.auth.models import User
from settings.base import MINNING_URLS

logger = logging.getLogger('sentry.errors')

def createTobToken(username, token, server, is_active=True, subed=None, valid=None, email=None):
    _server = server
    _username = username
    _token = token
    _is_active=is_active
    # _email = "" if type(email) != str else email
    # _subed = subed
    # _valid = valid
    tobToken = TobToken(username=_username, token=_token, server=_server, is_active=_is_active)
    try:
        tobToken.save()
    except Exception as e:
        logger.error("TobToken for username %s failed to be saved", _username)

    logger.info("Created TobToken for username %s",_username)


def createTobTokenAndInviteUserToRegister(server, email, username, token, subed, valid):
    # tobToken = createTobToken(server=server, email=email, token=token, username=username, subed=subed)
    # _email = "" if type(email) != str else email
    # TODO: Add invitation system to this system
    # logger.info("Created User % for email %s", _email)
    raise NotImplementedError()


def verifyTobToken(username, token):
    url = MINNING_URLS["Track-o-Bot"]
    try:
        response = requests.get(url, data={'page': 1, 'username': username, 'token': token})
        data = json.loads(response.text())
        return True if len(data['meta'].keys()) else False

    except Exception as e:
        logging.error(e)
        return None


def createUserFromTobToken(tobToken, userData):
    if len(User.objects.filter(email=userData.email)) == 0:
        newUser = User(username=userData.username,
                       first_name=userData.first_name,
                       last_name=userData.last_name,
                       email=userData.email,
                       is_active=True)
        newUser.profile.account_type=('f', 'Free')
        newUser.profile.partner_sub=userData.partner_sub
        newUser.profile.newsletter_sub=userData.newsletter_sub
        newUser.save()

        tobToken.user=newUser
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
        logger.debug("tob token {} of {} - username {} - account {}".format(i, len(sqlret), row.username, row.account))
        yield row


def posixConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to posix time"""
    d = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')
    return int(time.mktime(d.timetuple()))


def datetimeConversion(date='2016-12-02T02:29:09.000Z'):
    """Convert timestamp to datetime"""
    return datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.000Z')


def saveMatch(match_id, match_mode, user, date, blue_rank, blue_hero, blue_deck, red_hero, red_deck, turns_played,
               red_starts, blue_won, cards):

    # First check if the match exists
    try:
        match = Match.objects.get(match_id=match_id)
        userlist = [a for a in match.user.all()]
        if user in userlist:
            return
        else:
            match.user.add(user)
            compare_cards_and_update(match, user, cards)
            logger.info("New match entry for the database, match_id={}".format(match_id))
            return

    except Exception as e:
        logger.info("New match entry for the database, match_id={}".format(match_id))

    # if the match is here, add the user to it if he is not null
    # add the cards to it related to the match

    match = Match(
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
        blue_won = blue_won
    )

    try:
        match.save()
        # add user if present
        if user:
            match.user.add(user)

        # save cards
        for card in cards:
            if card['player'] == 'me':
                blueCard = CardPlayed(match=match, card=str(card['card']['id']),
                                       turn_played = card['turn'], is_spawned=False, user=user)
                blueCard.save()
                match.blue_played_cards.add(blueCard)
            else:
                redCard = CardPlayed(match=match, card=str(card['card']['id']),
                                       turn_played=card['turn'], is_spawned=False)
                redCard.save()
                match.red_played_cards.add(redCard)

        match.save()

    except Exception as e:
        logger.error("An unexpected error occured", e)


def compare_cards_and_update(match, user, cards):
    ''' Assigns an user to either the blue set of cards
     or red set of card in a preexistant match '''
    blueCards = [ int(b.id) for b in match.blue_played_cards.all()]
    redCards = [ int(r.id) for r in match.red_played_cards.all()]
    userCards = [ int(c['card']['id']) for c in cards if c['player']=='me']

    if len(set(blueCards) & set(userCards)) > len(set(redCards) & set(userCards)):
        # SET ALL BLUE CARDS AS BEING FOR USER
        blue_cards = match.blue_played_cards.all()
        for card in blue_cards:
            card.user = user
            card.save(update_fields=['user'])
    else:
        # SET ALL BLUE CARDS AS BEING FOR USER
        red_cards = match.red_played_cards.all()
        for card in red_cards:
            card.user = user
            card.save(update_fields=['user'])