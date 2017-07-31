# This service captures the data using Dora R. as base
# coding: utf-8
import os
import json
import logging
import requests
from arquivo.dao import tobTokenDAO
from django.db.utils import IntegrityError
from settings.base import MINNING_URLS

logger = logging.getLogger('sentry.errors')


def createTobToken(username, token, server, is_active=True):
    tobToken = tobTokenDAO.tobToken(username=username, token=token, server=server, is_active=is_active)
    try:
        tobToken.save()
        logger.info("Created TobToken for username %s", username)
    except Exception as e:
        logger.info("TobToken for username %s failed to be saved", username)
        raise IntegrityError("TobToken for username " + username + " failed to be saved")

    return tobToken

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
    sqlret = tobTokenDAO.findAllValidTokens(limit)

    logger.debug("{} tob tokens retrieved from database".format(len(sqlret)))

    for i, row in enumerate(sqlret):
        logger.debug("tob token {} of {} - username {} - account {}".format(i, len(sqlret), row.username, row.user))
        yield row


def getAllTobTokensYield(limit : int=0):
    """Get username, token and account from database"""
    sqlret = tobTokenDAO.findAll(limit)

    logger.debug("{} tob tokens retrieved from database".format(len(sqlret)))

    for i, row in enumerate(sqlret):
        logger.debug("tob token {} of {} - username {} - account {}".format(i, len(sqlret), row.username, row.user))
        yield row

