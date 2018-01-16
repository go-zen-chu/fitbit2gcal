#!/usr/bin/env python
import os
from fitbit2gcal import fitbit2gcal, fitbit_cred, fitbit_api
from datetime import datetime, timedelta
import argparse
from dateutil import parser as dt_parser

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sending Fitbit data to Google Calendar')

    # fitbit
    parser.add_argument('--fb_client', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_CLIENT"), help='Fitbit API oauth2 client')
    parser.add_argument('--fb_secret', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_SECRET"), help='Fitbit API oauth2 secret')
    parser.add_argument('--fb_access_token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN"), help='Fitbit API oauth2 access token')
    parser.add_argument('--fb_refresh_token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN"), help='Fitbit API oauth2 refresh token')
    parser.add_argument('--fb_expires_at', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_EXPIRES_AT"), help='Fitbit API oauth2 access token expires at')
    # google calendar
    parser.add_argument('--gcal_sleep_id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_SLEEP_ID"), help='Google Calendar storing sleep event')
    parser.add_argument('--gcal_activity_id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID"), help='Google Calendar storing activity event')

    default_time_zone = os.getenv("FITBIT2CAL_TIME_ZONE")
    default_time_zone = "UTC" if default_time_zone == None else default_time_zone
    parser.add_argument('--time_zone', type=str, default=default_time_zone, help='Time zone for Google Calendar')
    # datetime
    yesterday = datetime.today() - timedelta(days=1)
    parser.add_argument('--data_day', type=str, default=yesterday.strftime('%Y-%m-%d'), help='Date to store event in YYYY-mm-dd')
    parser.add_argument('--from_date', type=str, help='From day to store event in YYYY-mm-dd')
    parser.add_argument('--until_date', type=str, help='Until day to store event in YYYY-mm-dd')

    args = parser.parse_args()

    fb_cred = fitbit_cred.FitbitCred(args.fb_client, args.fb_secret, args.fb_access_token, args.fb_refresh_token, args.fb_expires_at)

    if args.from_date == None and args.until_date == None:
        # convert str -> datetime
        data_day = dt_parser.parse(args.data_day)
        fitbit2gcal.send_fb_events2gcal(
            fb_cred,
            args.gcal_sleep_id,
            args.gcal_activity_id,
            data_day=data_day,
            time_zone=args.time_zone)
    else:
        #TODO: get fitbit data in range
        pass
