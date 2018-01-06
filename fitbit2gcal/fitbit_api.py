#!/usr/bin/env python
import os
import sys
import json
import fitbit
from datetime import datetime, timedelta
from dateutil import parser

def auth_fitbit(fitbit_cred, unit=fitbit.Fitbit.METRIC):
    """
    Get authed client from fitbit using credentials.
    """
    try:
        authd_client = fitbit.Fitbit(
            fitbit_cred.client_id,
            fitbit_cred.client_secret,
            system=unit,
            access_token=fitbit_cred.access_token,
            refresh_token=fitbit_cred.refresh_token)
        # for testing whether client is authorized
        devs = authd_client.get_devices()
        print('Authorize Success! You are using {0}'.format(devs))
        return authd_client, None
    except Exception as err:
        return None, err

def get_sleeps(authd_client, datetime):
    sleepData = authd_client.get_sleep(datetime)
    return sleepData['sleep']

def get_activity_summary(authd_client, datetime):
    # - for user_id of current user.
    # https://dev.fitbit.com/reference/web-api/activity/#get-daily-activity-summary
    # this endpoint only retreive summary so there is no auto_detected data
    url = "{0}/{1}/user/-/activities/date/{2}.json".format(fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION, datetime.strftime('%Y-%m-%d'))
    res = authd_client.make_request(url)
    if res == None or res == "":
        return None
    else:
        return res['activities']

def get_activities_after(authd_client, after_date, sort="asc", limit=20):
    # - for user_id of current user.
    # https://dev.fitbit.com/reference/web-api/activity/
    url = "{0}/{1}/user/-/activities/list.json".format(fitbit.Fitbit.API_ENDPOINT, fitbit.Fitbit.API_VERSION)
    params = {
        "afterDate": after_date.strftime("%Y-%m-%d"),
        "sort": sort,
        "limit": limit,
        "offset": 0, # required just for now
    }
    # params will be set in **kwargs of request constructor
    res = authd_client.make_request(url, method="GET", params=params)
    if res == None or res == "":
        return None
    return res['activities']

def get_activities_of_date(authd_client, datetime):
    activities = get_activities_after(authd_client, datetime)
    if activities == None:
        return None
    in_date_activities = []
    for activity in activities:
        start_datetime = parser.parse(activity["startTime"])
        # ignore other date data
        if start_datetime.date() != datetime.date():
            continue
        in_date_activities.append(activity)
    return in_date_activities

def get_data_in_range(authd_client, from_date, to_date, data_fetch_func):
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
