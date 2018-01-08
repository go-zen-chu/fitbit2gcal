#!/usr/bin/env python
import os
from fitbit2gcal import fitbit2gcal, fitbit_cred
from datetime import datetime, timedelta
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sending Fitbit data to Google Calendar')

    # fitbit
    parser.add_argument('--fb_client', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_CLIENT"), help='Fitbit API oauth2 client')
    parser.add_argument('--fb_secret', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_SECRET"), help='Fitbit API oauth2 secret')
    parser.add_argument('--fb_access_token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_ACCESS_TOKEN"), help='Fitbit API oauth2 access token')
    parser.add_argument('--fb_refresh_token', type=str, required=True, default=os.getenv("FITBIT2CAL_FB_REFRESH_TOKEN"), help='Fitbit API oauth2 refresh token')
    # google calendar
    parser.add_argument('--gcal_sleep_id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_SLEEP_ID"), help='Google Calendar storing sleep event')
    parser.add_argument('--gcal_activity_id', type=str, required=True, default=os.getenv("FITBIT2CAL_GCAL_ACTIVITY_ID"), help='Google Calendar storing activity event')
    default_time_zone =  os.getenv("FITBIT2CAL_TIME_ZONE")
    default_time_zone = "UTC" if default_time_zone == None else default_time_zone
    parser.add_argument('--time_zone', type=str, default=default_time_zone, help='Time zone for Google Calendar')
    # datetime
    yesterday = datetime.today() - timedelta(days=1)
    default_data_day
    parser.add_argument('--data_day', type=str, default= help='Date to store event in YYYY-mm-dd')
    parser.add_argument('--from', type=str, help='From day to store event in YYYY-mm-dd')
    parser.add_argument('--until', type=str, help='Until day to store event in YYYY-mm-dd')

    args = parser.parse_args()

    fb_cred = fitbit_cred.FitbitCred(args.fb_client, args.fb_secret, args.fb_access_token, args.fb_refresh_token)

    if args.data_day != None:
        fitbit2gcal.register_fitbit_to_gcal(
            fb_cred,
            args.gcal_sleep_id,
            args.gcal_activity_id,
            data_day=args.data_day,
            time_zone=time_zone)
