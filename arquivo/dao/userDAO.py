import logging
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

logger = logging.getLogger('sentry.errors')


def findUserByEmail(email):
    try:
        return User.objects.filter(email=email)[0]
    except Exception as e:
        return None


def findUserByUsername(username):
    try:
        return User.objects.filter(username=username)[0]
    except Exception as e:
        return None


def createUser(username, password, first_name="", last_name="", email="", is_staff=False, is_active=True):
    user = User(username=username,
         first_name=first_name,
         last_name=last_name,
         email=email,
         password=password,
         is_staff=is_staff,
         is_active=is_active)
    user.save()
    return user

def createProfileForUser(user, account_type, partner_sub, newsletter_sub):
    try:
        user.profile.account_type=account_type
        user.profile.partner_sub=partner_sub
        user.profile.newsletter_sub=newsletter_sub
        user.save()
    except Exception as e:
        logger.error(e)
        raise IntegrityError("An error occurred while trying to set user {} profile".format(user))
