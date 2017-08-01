from django.db.models.query import QuerySet
import logging
from doraR.doraR import DoraR
from arquivo.services import tobTokenServices
# This service comunicates with DoraR, running processes, opening new jobs, etc.

logger = logging.getLogger('sentry.errors')


def startDoraR(tobTokenList: QuerySet = None, workers: int = 4, past_days: int = 7, ranked_only: bool = True ):
    '''Start DoraR in threads, but running in N threads, with N tokens for each'''

    if not tobTokenList:
        tobTokenList = tobTokenServices.getAllValidTobTokens()

    W = []

    step = len(tobTokenList) // workers

    logger.info("Starting %d workers, each running about ~%d tokens, with about %d past days", workers, step, past_days)

    if step == 0 :
        DoraR.runOnThread(list(tobTokenList))
    else:
        for i in range(workers):
            W.append(DoraR(past_days=past_days, ranked_only=ranked_only))
            if (i == (workers-1)) or ((i+1)*step > len(tobTokenList)):
                W[-1].runOnThread(list(tobTokenList[i * step:]))
            else:
                W[-1].runOnThread(list(tobTokenList[i * step:(i + 1) * step]))


def startDoraRForToken(tobToken):
    '''Star DoraR in a single thread for 1 token'''
    DoraR.runOnThread(tobToken)