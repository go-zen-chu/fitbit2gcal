#!/usr/bin/env python
import os
import sys
import json
import fitbit
from datetime import timedelta

class FitbitAPI:
    def __init__(self):
        # specify US if you prefer
        self.UNIT=fitbit.Fitbit.METRIC

    def auth_fitbit(self, client_id, client_secret, access_token, refresh_token):
        """
        Get authed client from fitbit using credentials.
        """
        try:
            authd_client = fitbit.Fitbit(
                client_id,
                client_secret,
                system=self.UNIT,
                access_token=access_token,
                refresh_token=refresh_token)
            # for testing whether client is authorized
            devs = authd_client.get_devices()
            print('Authorize Success! You are using {0}'.format(devs))
            return authd_client, None
        except Exception as err:
            return None, err

    def get_sleeps(self, authd_client, datetime):
        sleepData = authd_client.get_sleep(datetime)
        return sleepData['sleep']

    def get_activities(self, authd_client, datetime):
        # - for user_id of current user.
        url = "{0}/{1}/user/{2}/activities/date/{3}.json".format(fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION, '-', datetime.strftime('%Y-%m-%d'))
        res = authd_client.make_request(url)
        if res == None or res == "":
            return None
        else:
            return res['activities']

    def get_data_in_range(self, authd_client, from_date, to_date, data_fetch_func):
        '''
        Get data using data_fetch_func from_date to to_date
        '''
        date_diff = (to_date - from_date).days
        if date_diff <= 0:
            return None, Exception('Date difference is invalid')
        data_list = []
        # +1 for to_date
        #pb = ProgressBar() # just wrap iterable
        for i in range(date_diff + 1):
            parsing_date = from_date + timedelta(days=i)
            print(parsing_date)
            # array of sleep, since you can sleep mulitply in a day
            data_of_day = data_fetch_func(authd_client, parsing_date)
            if data_of_day != None:
                for datum in data_of_day:
                    data_list.append(datum)
            else:
                print('No data find in {0}. Skipping'.format(parsing_date))
        return data_list, None
