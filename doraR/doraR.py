# coding: utf-8
import json
import time
import logging
import requests
import argparse
import pandas as pd
from threading import Thread
from datetime import datetime, timedelta
from arquivo.services import posixConversion, datetimeConversion, getValidTobTokensYield, saveMatch
from settings.base import MINNING_URLS


class DoraR():
    logger = logging.getLogger('sentry.errors')

    def __init__(self, verbose=False, past_days=7, max_retries=3, ranked_only=True, limit=None):
        self.from_date = datetime.today() - timedelta(days=past_days)
        self.past_days = past_days
        self.max_retries = max_retries
        self.ranked_only = ranked_only
        self.limit = limit
        self.logger.info("Starting Dora R. from %s until today", self.from_date)
        self.url = MINNING_URLS["Track-o-Bot"]

    def getAllDataFromSingleToken(self, tob_token):
        game_data_history = self.getTobData(tob_token=tob_token)
        self.matchEntryGenerator(tob_token=tob_token, game_data_history=game_data_history)

    def getTobData(self, tob_token, override_limit_date=False):
        """Actually downloads the raw data from track o bot"""
        from_date = time.mktime(self.from_date.timetuple())

        page = 1
        end = False
        data_history = []
        try_and_error = self.max_retries
        while (True):
            try:
                response = requests.get(self.url, data={ "page": page, "username": tob_token.username, "token": tob_token.token })
                self.logger.debug("username %s - page %d - account %s",tob_token.username, page, tob_token.user)

            except Exception as e:
                self.logger.error(
                    "Failure trying to get data from username %s, " +
                    "repeats remaing for this user: %d, failure due to %s"
                    ,tob_token.id, try_and_error, e)

                if try_and_error:
                    try_and_error -= 1
                    continue
                else:
                    # maybe should maybe set the token as invalid...
                    break

            try:
                resp = response.text
                data = json.loads(resp)
                try_and_error = self.max_retries
            except Exception as e:
                try_and_error -= 1
                continue

            # This line allows you to get all data, not matter how long ago it was created
            if not override_limit_date:
                for n in range(len(data['history'])):
                    # Remove data that is older than the data we are looking for so we free up some memory
                    if posixConversion(data['history'][n]['added']) < from_date:
                        del data['history'][n:len(data['history'])]
                        end = True
                        break

            data_history += data['history']

            if self.limit:
                return data_history

            # end of the loop
            # has some magic numbers, but believe me, it work wonders
            if data['meta']['total_pages'] <= data['meta']['current_page'] or end or page > ((400 * self.past_days) // 25):
                break

            page += 1

            self.logger.info("Captured %d matchs in this given time window from %s to today",len(data_history), self.from_date)

        return data_history

    def matchEntryGenerator(self, tob_token, game_data_history):
        """Get the data from track-o-bot and sets it up to save in our database"""

        def get_turns(data):
            """Get the total number of turns played in the match"""
            a = 0
            for i in range(len(data)):
                a = data[i]['turn'] if data[i]['turn'] > a else a
            return a

        # =========================================
        # Start of match_entry_generator
        total_entries = 0

        df = pd.DataFrame(columns=['match_id', 'match_mode', 'user', 'date', 'blue_rank', 'blue_hero', 'blue_deck',
                                   'red_hero', 'red_deck', 'turns_played', 'red_starts', 'blue_won', 'cards_played'])
        # Run the loop capturing data from track-o-bot
        for i, game in enumerate(game_data_history):

            if game['mode'] != 'ranked' and self.ranked_only:
                continue

            df.loc[i] = [
                    int(game['id']),
                    game['mode'],
                    tob_token.user,
                    datetimeConversion(game['added']),
                    None if game['rank'] is None else int(game['rank']),
                    game['hero'],
                    game['hero_deck'],
                    game['opponent'],
                    game['opponent_deck'],
                    get_turns(game['card_history']),
                    True if game['coin'] else False,
                    True if game['result'] == 'win' else False,
                    game['card_history']
                ]

        df[['blue_rank']] = df[['blue_rank']].fillna(method='ffill')
        df[['blue_rank']] = df[['blue_rank']].fillna(20)

        for index, entry in df.iterrows():
            saveMatch(match_id=entry['match_id'],
                        match_mode=entry['match_mode'],
                        user=entry['user'],
                        date=entry['date'],
                        blue_rank=entry['blue_rank'],
                        blue_hero=entry['blue_hero'],
                        blue_deck=entry['blue_deck'],
                        red_hero=entry['red_hero'],
                        red_deck=entry['red_deck'],
                        turns_played=entry['turns_played'],
                        red_starts=entry['red_starts'],
                        blue_won=entry['blue_won'],
                        cards=entry['cards_played'])
            total_entries += 1

        self.logger.info("Saved a total of %d games",total_entries)
        return

    def runOnExecutor(self):
        """Runs Starseeker in a thread, necessary since it takes alot of time to run"""
        self.logger.info("Starting Dora R. Thread")
        Thread(target=self.start_auto).start()

    def startAuto(self):
        for tob_token in getValidTobTokensYield():
            print(tob_token)
            game_data_history = self.getTobData(tob_token=tob_token)
            print("found {} games".format(len(game_data_history)))
            self.matchEntryGenerator(tob_token=tob_token, game_data_history=game_data_history)


if __name__ == '__main__':
    """In case this is run manually"""
    parser = argparse.ArgumentParser(description='mine data from trackobot')
    parser.add_argument('-d', '--past_days', type=int, default='2',
                        help='how long ago is the last relevant game played by a player')
    args = parser.parse_args()

    D = DoraR(past_days=args['past_days'])
    D.runOnExecutor()